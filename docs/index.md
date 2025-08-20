# Welcome to django-xchange

This is the documentation for the django-xchange library.

`django-xchange` is a Django library for managing currency exchange rates.

## Features

*   Fetch exchange rates from various brokers.
*   Store exchange rates in your Django database.
*   Easy to extend with custom brokers.

## Demo

A demo Django application is provided in tests/demo folder.

To set it up run once `python manage.py demo`

It will:
1. create if not exists yet a sqlite database and launch migrations
2. Create if not exists yet a superuser ( username: admin, password: 123)
3. Populate the database with some example exchange rates


To run the demo server: `python manage.py runserver` and go to http://127.0.0.1:8000/

### API

A basic REST API is implemented with basic Django views at _src/django_xchange/views.py_

You can test it with [httpie](https://httpie.io/) (provided by the development dependencies).

Get the list of rates:
```shell
# List of rates
http localhost:8000/rate/

# Add a rate
http POST localhost:8000/rate/ day=2022-01-09 base=EUR rates[EUR]=0.838 rates[USD]=1

# To get a rate if it exists
http GET localhost:8000/rate/2022-01-09/

# To get a rate even if it not exists as record yet. This will contact the brokers to get the rate.
http GET localhost:8000/rate/2022-01-08/?force=1

# To update
http PUT localhost:8000/rate/2022-01-09/ base=GBP rates[EUR]=0.838 rates[USD]=2

# To delete
http DELETE localhost:8000/rate/2022-01-09/
```
