from typing import TypedDict, TypeVar

from django.conf import settings
from django.utils.translation import gettext as _

from django_xchange.exceptions import ConfigurationError
from django_xchange.types import BrokerType

_DEFAULT_SETTINGS = {'BASE_CURRENCY': 'EUR', 'CURRENCIES': ['USD', 'EUR', 'GBP'], 'BROKERS': []}


class ConfigType(TypedDict):
    BASE_CURRENCY: str
    CURRENCIES: list[str]
    BROKERS: list[BrokerType]

class Config[ConfigType]:
    def __init__(self) -> None:
        self.conf = _DEFAULT_SETTINGS | getattr(settings, 'DJANGO_XCHANGE', {})
        if not self.conf.get('BROKERS'):
            raise ConfigurationError(_('No brokers configured'))

    def __getattr__(self, item: str) -> object:
        if item := self.conf.get(item):
            if callable(item):
                return item()
            else:
                return item
        raise AttributeError(item)


config: Config = Config()
