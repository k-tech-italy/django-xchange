from datetime import date, timedelta

import factory
from factory.base import FactoryMetaClass
from factory.fuzzy import FuzzyDecimal


factories_registry = {}


class AutoRegisterFactoryMetaClass(FactoryMetaClass):
    def __new__(cls, class_name, bases, attrs):
        new_class = super().__new__(cls, class_name, bases, attrs)
        factories_registry[new_class._meta.model] = new_class
        return new_class


class AutoRegisterModelFactory(factory.django.DjangoModelFactory, metaclass=AutoRegisterFactoryMetaClass):
    pass


def get_factory_for_model(_model):
    class Meta:
        model = _model

    if _model in factories_registry:
        return factories_registry[_model]
    return type(f'{_model._meta.model_name}AutoFactory', (AutoRegisterModelFactory,), {'Meta': Meta})


class RateFactory(factory.django.DjangoModelFactory):
    day = factory.Faker(
        'date_between_dates',
        date_start=date(2020, 1, 1),
        date_end=date(2022, 12, 31),
    )

    class Meta:
        model = 'django_xchange.Rate'
