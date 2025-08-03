import typing


from django_xchange.brokers import Broker

if typing.TYPE_CHECKING:
    from decimal import Decimal
    from datetime import date


class BadBroker(Broker):
    def get_rates(self, day: 'date', symbols: list[str] = None) -> dict[str, 'Decimal']:
        raise NotImplementedError('_dummy_')
