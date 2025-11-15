import pytest
import responses


@pytest.fixture
def mock_config(monkeypatch) -> None:
    def fx(**overrides):
        monkeypatch.setattr('django_xchange.config.Config._parse_env', lambda x: overrides)

    return fx


@pytest.fixture
def mock_pyoxr_provider(mock_config, monkeypatch, settings):
    settings.DJANGO_XCHANGE['BROKERS'] = ['django_xchange.brokers.pyoxr.PyoxrBroker']

    from django.utils.http import urlencode
    from pyoxr import OXRClient

    OXRClient.default_api = OXRClient(app_id='123')

    from django_xchange.brokers.pyoxr import PyoxrBroker

    PyoxrBroker._initialised = True

    def fx(day, requested, retrieved):
        responses.add(
            responses.GET,
            f'https://openexchangerates.org/api/historical/{day:%Y-%m-%d}.json?'
            + urlencode({'app_id': 123, 'symbols': requested}),
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
