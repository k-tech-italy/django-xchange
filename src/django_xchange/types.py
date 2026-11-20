import typing
from abc import abstractmethod
from decimal import Decimal

if typing.TYPE_CHECKING:
    from datetime import date


@typing.runtime_checkable
class BrokerProtocol(typing.Protocol):
    @abstractmethod
    def get_rates(self, day: 'date', symbols: list[str]) -> dict[str, Decimal]:
        raise NotImplementedError()


# A broker is configured either as a fully-qualified class name or as the class itself
BrokerType: typing.TypeAlias = 'str | type[BrokerProtocol]'
