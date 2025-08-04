from datetime import date
from decimal import Decimal

import pytest
import responses
from testutils.factories import RateFactory


def test_rate_str(db):
    rate = RateFactory()
    assert str(rate) == f'{rate.day:%Y-%m-%d}'


@pytest.fixture(autouse=True)
def pyoxr(settings):
    settings.OPEN_EXCHANGE_RATES_APP_ID = ''
    settings.DJANGO_XCHANGE = {'BROKERS': ['django_xchange.brokers.pyoxr.PyoxrBroker']}


@responses.activate
@pytest.mark.django_db
@pytest.mark.parametrize(
    'initial, refresh, include, requested, expected',
    [
        pytest.param(None, False, None, 'EUR,GBP,USD', {'EUR': 1.0, 'GBP': 0.839441, 'USD': 1.084928}, id='empty'),
        pytest.param(
            {'ABC': 0.9, 'GBP': 1.1},
            False,
            None,
            'EUR,USD',
            {'ABC': 0.9, 'EUR': 1.0, 'GBP': 1.1, 'USD': 1.084928},
            id='existing',
        ),
        pytest.param(
            {'EUR': 0.9, 'GBP': 1.1},
            False,
            ['GBP'],
            'EUR,USD',
            {'EUR': 0.9, 'GBP': 1.1, 'USD': 1.084928},
            id='not-overwrite',
        ),
        pytest.param(
            {'GBP': 1.1}, True, None, 'EUR,GBP,USD', {'EUR': 1.0, 'GBP': 0.839441, 'USD': 1.084928}, id='force'
        ),
    ],
)
def test_rate_for_day(initial, refresh, include, requested, expected, mock_rate_provider):
    from django_xchange.models import Rate

    assert Rate.objects.count() == 0

    day = date(2022, 5, 7)

    mock_rate_provider(
        day,
        requested,
        {k: v for k, v in {'EUR': 0.92172, 'GBP': 0.77373, 'USD': 1}.items() if k in requested.split(',')},
    )

    if initial:
        RateFactory(day=day, rates=initial)
    rate = Rate.for_date(day, refresh=refresh, include=include)

    assert rate.day == day
    assert rate.rates == expected

    assert Rate.objects.count() == 1
    rate.refresh_from_db()
    assert rate.rates == expected


@responses.activate
@pytest.mark.django_db
@pytest.mark.parametrize(
    'from_value, from_currency, to_currency, expected',
    [
        pytest.param(1, 'USD', 'USD', Decimal('1'), id='usd-usd'),
        pytest.param(1, 'USD', 'EUR', Decimal('0.20'), id='usd-eur'),
        pytest.param(1, 'EUR', 'USD', Decimal('5.0'), id='eur-usd'),
        pytest.param(1, 'USD', 'GBP', Decimal('2'), id='usd-gbp'),
        pytest.param(1, 'GBP', 'EUR', Decimal('0.1'), id='gbp-eur'),
        pytest.param(1, 'EUR', 'GBP', Decimal('10'), id='eur-gbp'),
        pytest.param(1, 'GBP', None, Decimal('0.1'), id='gbp-default'),
    ],
)
def test_rate_convert(from_value, from_currency, to_currency, expected):
    from django_xchange.models import Rate

    rate = Rate(day=date(2022, 5, 7), rates={'EUR': 0.2, 'GBP': 2, 'USD': 1})

    result = rate.convert(from_value, from_currency, to_currency=to_currency, force=False)
    assert result == expected
    assert isinstance(result, Decimal)


@responses.activate
@pytest.mark.parametrize(
    'ensured, force, include, expected',
    [
        pytest.param(
            {'EUR': 0.92172, 'GBP': 0.77373, 'USD': 1}, False, None, {'EUR': 0.2, 'GBP': 2, 'USD': 1}, id='empty'
        ),
        pytest.param(
            {'EUR': 0.92172, 'GBP': 0.77373, 'USD': 1},
            True,
            None,
            {'EUR': 1, 'GBP': 0.839441, 'USD': 1.084928},
            id='force',
        ),
    ],
)
def test_rate_get_rates(ensured, force, include, expected, monkeypatch, mock_rate_provider):
    from django_xchange.models import Rate

    day = date(2022, 5, 7)

    rate = Rate(day=day, base='USD', rates={'EUR': 0.2, 'GBP': 2, 'USD': 1})

    if force:
        mock_rate_provider(day, 'EUR,GBP,USD', {'EUR': 0.92172, 'GBP': 0.77373, 'USD': 1})

        rate.rates = ensured

    result = rate.get_rates(force=force, include=include)

    assert result == {k: round(Decimal(v), 7) for k, v in expected.items()}
