from decimal import Decimal

import pytest

from django_xchange.brokers import Broker
from django_xchange.utils import resolve_fqn
from exceptions import ConfigurationError


def test_no_brokers(settings):
    settings.DJANGO_XCHANGE = {'BROKERS': []}

    with pytest.raises(ConfigurationError, match='No brokers configured'):
        _ = Broker().get_rates('2022-01-01')


def test_bad_brokers(settings):
    settings.DJANGO_XCHANGE = {'BROKERS': ['testutils.bad_broker.BadBroker']}

    with pytest.raises(RuntimeError, match='No rates available'):
        _ = Broker().get_rates('2022-01-01')
