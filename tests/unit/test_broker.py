from decimal import Decimal as D
from contextlib import nullcontext as does_not_raise

import pytest

from django_xchange.brokers import BrokerManager
from django_xchange.exceptions import ConfigurationError
from testutils.test_brokers import DummyBroker


@pytest.fixture
def mock_broker(monkeypatch) -> None:
    class MockedConfig:
        pass

    monkeypatch.setattr('django_xchange.config.Config', MockedConfig)
    yield


def test_no_brokers(settings):
    settings.DJANGO_XCHANGE = {'BROKERS': []}

    with pytest.raises(ConfigurationError, match='No brokers configured'):
        _ = BrokerManager().get_rates('2022-01-01')


def test_bad_brokers(settings):
    settings.DJANGO_XCHANGE = {'BROKERS': ['testutils.bad_broker.BadBroker']}

    with pytest.raises(RuntimeError, match='No rates available'):
        _ = BrokerManager().get_rates('2022-01-01')


@pytest.mark.parametrize(
    'base_curr, expectation, result',
    [
        pytest.param('EUR', does_not_raise(), {'AAA': 0.333333, 'BBB': 0.666667, 'EUR': 1.0}, id='EUR'),
        pytest.param('AAA', does_not_raise(), {'AAA': 1, 'BBB': 2, 'EUR': 3}, id='AAA'),
    ],
)
def test_brokers_ok(base_curr, expectation, result, settings):
    settings.DJANGO_XCHANGE = {
        'BROKERS': lambda : [DummyBroker],
        'BASE_CURRENCY': base_curr,
    }
    with expectation:
        assert BrokerManager().get_rates('2022-01-01') == result | {
            '_base': base_curr,
            '_provider': 'testutils.bad_broker.DummyBroker',
        }

    # settings.DJANGO_XCHANGE = {'BROKERS': [lambda: fqn('testutils.bad_broker.DummyBroker')]}
    # assert Broker().get_rates('2022-01-01') == {'AAA': D(1), 'BBB': D(2), 'EUR': D(3)}
