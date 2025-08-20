# Configuration

This section describes how to configure `django-xchange`.

## Settings

You can configure `django-xchange` in your Django `settings.py` file.

Here is an example of the available settings:

```python
XCHANGE_APP_ID = "your-app-id"
XCHANGE_BASE_CURRENCY = "USD"
XCHANGE_BROKER = [
    "django_xchange.brokers.pyoxr.PyOXRBroker",
]
```
