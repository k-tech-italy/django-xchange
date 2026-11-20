import typing
from decimal import Decimal
from gettext import gettext as _

from django_xchange.utils import resolve_fqn
from django_xchange.exceptions import ConfigurationError

if typing.TYPE_CHECKING:
    from django_xchange.types import BrokerProtocol
    from datetime import date


class BrokerManager:
    def get_rates(self, day: 'date', symbols: list[str] | None = None) -> dict[str, typing.Any]:
        """Return the rates from the first configured broker that succeeds.

        Besides the currency rates, the result holds metadata keys prefixed with `_` (e.g. `_base`).
        """
        from django_xchange.config import get_config, get_base_currency

        if not (brokers := get_config().BROKERS):
            raise ConfigurationError(_('No brokers configured'))
        for broker in brokers:
            try:
                broker_class: type[BrokerProtocol] = resolve_fqn(broker) if isinstance(broker, str) else broker
                rates: dict[str, typing.Any] = broker_class().get_rates(day, symbols or [])
                base = get_base_currency()
                if base != rates['_base']:
                    ratio = round(Decimal(1 / rates[base]), 8)
                    new_rates = {k: float(round(v * ratio, 6)) for k, v in rates.items() if not k.startswith('_')}
                    rates |= new_rates | {'_base': base}
                return rates
            except Exception:  # noqa: BLE001, S110, PERF203
                # TODO: think of better handling
                pass
        raise RuntimeError(_('No rates available'))
