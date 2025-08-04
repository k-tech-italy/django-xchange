# Models

This section describes the models used by `django-xchange`.

## ExchangeRate

The `ExchangeRate` model stores the exchange rates for a given currency pair.

It has the following fields:

*   `base_currency`: The base currency.
*   `target_currency`: The target currency.
*   `rate`: The exchange rate.
*   `updated_at`: The date and time when the exchange rate was last updated.
