import typing
from abc import abstractmethod
from datetime import date
from decimal import Decimal


@typing.runtime_checkable
class BrokerProtocol(typing.Protocol):
    @abstractmethod
    def get_rates(self, day: 'date', symbols: list[str]) -> dict[str, Decimal]:
        raise NotImplementedError()

type BrokerType = str | BrokerProtocol
