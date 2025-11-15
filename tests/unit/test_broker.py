from contextlib import nullcontext as does_not_raise

import pytest

from django_xchange.exceptions import ConfigurationError
from django_xchange.brokers.common import BrokerManager
from testutils.test_brokers import DummyBroker


def test_no_brokers(mock_config):
    mock_config(BROKERS=[])

    with pytest.raises(ConfigurationError, match='No brokers configured'):
        _ = BrokerManager().get_rates('2022-01-01')


def test_bad_brokers(mock_config):
    mock_config(BROKERS=['testutils.bad_broker.BadBroker'])

    with pytest.raises(RuntimeError, match='No rates available'):
        _ = BrokerManager().get_rates('2022-01-01')


@pytest.mark.parametrize(
    'base_curr, expectation, result',
    [
        pytest.param('EUR', does_not_raise(), {'AAA': 0.333333, 'BBB': 0.666667, 'EUR': 1.0}, id='EUR'),
        pytest.param('AAA', does_not_raise(), {'AAA': 1, 'BBB': 2, 'EUR': 3}, id='AAA'),
    ],
)
def test_brokers_ok(base_curr, expectation, result, mock_config):
    mock_config(BROKERS=lambda: [DummyBroker], BASE_CURRENCY=base_curr)
    with expectation:
        assert BrokerManager().get_rates('2022-01-01') == result | {
            '_base': base_curr,
            '_provider': 'testutils.bad_broker.DummyBroker',
        }
