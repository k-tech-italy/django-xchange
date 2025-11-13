import typing

from decimal import Decimal
from random import random

from django_xchange.types import BrokerProtocol

if typing.TYPE_CHECKING:
    from datetime import date


class RandomBroker(BrokerProtocol):
    def get_rates(self, day: 'date', symbols: list[str]) -> dict[str, Decimal]:
        return {1.5 - random() for s in symbols} | {'_base': 'USD', 'USD': 1}
