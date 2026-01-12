# Configuration

This section describes how to configure `django-xchange`.

## Settings

You can configure `django-xchange` in your Django `settings.py` file.

Here is an example of the settings:

```python
INSTALLED_APPS = (
    [
        ...
        "django_xchange",
        ...
    ]

...

DJANGO_XCHANGE = {
    'BASE_CURRENCY': 'EUR',
    'CURRENCIES': ['USD', 'EUR', 'GBP'],
    'BROKERS': ['django_xchange.brokers.pyoxr.PyOXRBroker'],
}
```

## Broker configuration

See also the broker's documentation for the necessary settings and envrionment variables.
For example the PyOXR broker will require the OPEN_EXCHANGE_RATES_APP_ID
envrionment variable.