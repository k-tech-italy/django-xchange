import pytest

from django_xchange.config import Config, _DEFAULT_SETTINGS


def test_config_fx(settings) -> None:
    assert _DEFAULT_SETTINGS['CURRENCIES'] == Config().CURRENCIES

    settings.DJANGO_XCHANGE = {
        'CURRENCIES': lambda: ['A', 'B'],
    }

    assert Config().CURRENCIES == ['A', 'B']


def test_config_missing():
    with pytest.raises(AttributeError):
        _ = Config().DUMMY
