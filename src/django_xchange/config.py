import typing
from functools import lru_cache

from django.utils.translation import gettext as _
from django_xchange.exceptions import ConfigurationError
from django_xchange.types import BrokerType


class ConfigType(typing.Protocol):
    BASE_CURRENCY: str
    CURRENCIES: list[str]
    BROKERS: list[BrokerType]


class Config:
    _conf: typing.ClassVar[dict[str, typing.Any]] = {}

    def __init__(self) -> None:
        from django.conf import settings  # noqa: PLC0415

        Config._conf = getattr(settings, 'DJANGO_XCHANGE', {})
        if not Config._conf.get('BROKERS'):
            raise ConfigurationError(_('No brokers configured'))

    def __getattr__(self, item: str) -> object:
        if item in Config._conf:
            value = Config._conf[item]
            if callable(value):
                return value()
            return value
        raise AttributeError(item)


@lru_cache(maxsize=1)
def get_config() -> ConfigType:
    return typing.cast('ConfigType', Config())


def get_base_currency() -> str:
    return get_config().BASE_CURRENCY
