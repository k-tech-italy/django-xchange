from datetime import date

import pytest
import responses


def test_ratelist_get(client, db):
    from testutils.factories import RateFactory

    rate = RateFactory(day=date(2022, 5, 7), rates={'_base': 'EUR', 'EUR': 1.0})

    response = client.get('/rate/')

    assert response.status_code == 200
    assert response.json() == {'2022-05-07': {'base': rate.base, 'rates': {'_base': 'EUR', 'EUR': 1.0}}}


@pytest.mark.parametrize('method', ['put', 'patch', 'delete'])
def test_ratelist_method_not_allowed(client, db, method):
    response = getattr(client, method)('/rate/')

    assert response.status_code == 405
    assert response.json() == {'error': f'Method {method.upper()} not allowed'}


@pytest.mark.parametrize('method', ['post', 'patch'])
def test_rate_method_not_allowed(client, db, method):
    response = getattr(client, method)('/rate/2022-05-07/')

    assert response.status_code == 405
    assert response.json() == {'error': f'Method {method.upper()} not allowed'}


def test_rate_get_existing(client, db):
    from testutils.factories import RateFactory

    rate = RateFactory(day=date(2022, 5, 7), rates={'_base': 'EUR', 'EUR': 1.0})

    response = client.get('/rate/2022-05-07/')

    assert response.status_code == 200
    assert response.json() == {'2022-05-07': {'base': rate.base, 'rates': {'_base': 'EUR', 'EUR': 1.0}}}


@pytest.mark.parametrize('query', ['', '?force=', '?force=n', '?force=0'])
def test_rate_get_missing_not_forced(client, db, query):
    from django_xchange.models import Rate

    response = client.get(f'/rate/2022-05-07/{query}')

    assert response.status_code == 404
    assert response.json() == {'error': 'No record found for 2022-05-07'}
    assert not Rate.objects.exists()


@responses.activate
@pytest.mark.parametrize('force', ['1', 'y', 'Yes', 'true', 'T'])
def test_rate_get_missing_forced(client, db, mock_pyoxr_provider, force):
    from django_xchange.models import Rate

    day = date(2022, 5, 7)
    mock_pyoxr_provider(day, 'EUR,GBP,USD', {'EUR': 0.92172, 'GBP': 0.77373, 'USD': 1})

    response = client.get(f'/rate/2022-05-07/?force={force}')

    assert response.status_code == 200
    rates = response.json()['2022-05-07']['rates']
    assert rates['_base'] == 'EUR'
    assert rates['GBP'] == 0.839441
    assert Rate.objects.get().day == day
