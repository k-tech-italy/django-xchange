import datetime as dt
import typing
from collections.abc import Iterable
from decimal import Decimal

from django.db import models

from django.db import transaction

from django_xchange.config import get_base_currency


class Rate(models.Model):
    day = models.DateField(primary_key=True)
    base = models.CharField(max_length=3, help_text='Base rate (ISO3)', default=get_base_currency)
    rates = models.JSONField(default=dict)

    class Meta:
        ordering = ['day']

    def __str__(self) -> str:
        return str(self.day.strftime('%Y-%m-%d'))

    def get_rates(self, force: bool = False, include: Iterable[str] | None = None) -> dict[str, Decimal]:
        """Retrieve the rate values as Decimals. Forces the refresh if needed."""
        symbols = set(self.rates) | set(include or [])
        if force:
            rates = Rate.for_date(self.day, refresh=force, include=symbols).rates
        else:
            rates = self.rates
        return {k: round(Decimal(v), 7) for k, v in rates.items() if not k.startswith('_')}

    def convert(
        self, from_value: float | Decimal, from_currency: str, to_currency: str | None = None, force: bool = False
    ) -> Decimal:
        """Convert a value from a specific currency to another.

        If target currency is not specified it will be using settings.BASE_CURRENCY.

        :param from_value: The value to convert.
        :param from_currency: The currency to convert from in ISO3 format.
        :param to_currency: The currency to convert to in ISO3 format.
        :param force: Force refresh.

        :return: The converted value.
        """
        from django_xchange.config import get_config

        if not isinstance(from_value, Decimal):
            from_value = Decimal(from_value)

        if to_currency is None:
            to_currency = get_config().BASE_CURRENCY

        rates = self.get_rates(force=force, include=[from_currency, to_currency])
        return round(from_value / Decimal(rates[from_currency]) * Decimal(rates[to_currency]), 7)

    @staticmethod
    def for_date(day: dt.date, refresh: bool = False, include: Iterable[str] | None = None) -> 'Rate':
        """Constructor-like method returning a Rate instance for the specific date.

        It will always request the BASE_CURRENCY.

        :param day: Date to fetch the Rate instance
        :param refresh: to force refreshing values
        :param include: list of currencies to include in the request

        :return: Rate instance
        """
        from django_xchange.config import get_config

        with transaction.atomic():
            if include is None:
                include = []

            rate, _ = Rate.objects.get_or_create(day=day)
            if refresh:
                missing = set(get_config().CURRENCIES) | {get_config().BASE_CURRENCY} | set(include)
            else:
                missing = ((set(get_config().CURRENCIES) | set(include)) - set(rate.rates)) | {
                    get_config().BASE_CURRENCY
                }
            if missing:
                from django_xchange.brokers.common import BrokerManager

                client = BrokerManager()
                fetched_rates = client.get_rates(day, sorted(missing))
                if refresh:
                    rate.rates |= fetched_rates
                else:
                    rate.rates = fetched_rates | rate.rates
                rate.save()
            return rate

    def as_dict(self) -> dict[str, dict[str, typing.Any]]:
        return {self.day.strftime('%Y-%m-%d'): {'base': self.base, 'rates': self.rates}}
