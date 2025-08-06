# Models

This section describes the models used by `django-xchange`.

## Rate

The `Rate` model stores the exchange rates for a given currency pair.

It has the following fields:

*   `day`: The date the rates refer to.
*   `base`: The base currency for the rates.
*   `rates`: The exchange rates with respect to base currency.

The `Rate` model provides the following methods:

*   `for_date` [staticmethod]: An helper static method for fetching an
                              instance of a Rate.
*   `get_rates`: Gets the rates a dict[str, Decimal].
                The str is the currency iso3.
*   `convert`: Converts an amount from a currency to another.
