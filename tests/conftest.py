import pytest
import responses


@pytest.fixture
def mock_rate_provider(settings, db):
    from django.utils.http import urlencode

    def fx(day, requested, retrieved):
        responses.add(
            responses.GET,
            f'https://openexchangerates.org/api/historical/{day:%Y-%m-%d}.json?'
            + urlencode({'app_id': settings.OPEN_EXCHANGE_RATES_APP_ID, 'symbols': requested}),
            json={
                'disclaimer': 'Usage subject to terms: https://openexchangerates.org/terms',
                'license': 'https://openexchangerates.org/license',
                'timestamp': 1582588799,
                'base': 'USD',
                'rates': retrieved,
            },
            status=200,
        )

    return fx
