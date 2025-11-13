import os
import typing
from functools import lru_cache
from typing import TypedDict

from django.utils.translation import gettext as _
from django_xchange.exceptions import ConfigurationError
from django_xchange.types import BrokerType


_DEFAULT_CONFIG = {'BASE_CURRENCY': 'EUR', 'CURRENCIES': ['USD', 'EUR', 'GBP'], 'BROKERS': []}
_conf = None


class ConfigType(TypedDict):
    BASE_CURRENCY: str
    CURRENCIES: list[str]
    BROKERS: list[BrokerType]


class Config[ConfigType]:
    def __init__(self, **kwargs: typing.ParamSpecKwargs) -> None:
        from django.conf import settings

        self._conf = _DEFAULT_CONFIG | (getattr(settings, 'DJANGO_XCHANGE', {}) or {}) | self._parse_env() | kwargs
        if not self._conf.get('BROKERS'):
            raise ConfigurationError(_('No brokers configured'))

    def __getattr__(self, item: str) -> object:
        if item in self._conf:
            item = self._conf.get(item)
            if callable(item):
                return item()
            return item
        raise AttributeError(item)

    def _parse_env(self) -> dict[str, str]:
        env = {}
        if base_currency := os.environ.get('DJANGO_XCHANGE_BASE_CURRENCY', None):
            env['BASE_CURRENCY'] = base_currency
        if currencies := os.environ.get('DJANGO_XCHANGE_CURRENCIES', None):
            env['BASE_CURRENCY'] = currencies.split(',')
        if brokers := os.environ.get('DJANGO_XCHANGE_BROKERS', None):
            env['BROKERS'] = brokers.split(',')

        return env


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()


def get_base_currency() -> str:
    return get_config().BASE_CURRENCY
