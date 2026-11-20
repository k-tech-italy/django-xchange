from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import Rate


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('day', 'base')

    list_filter = (('day', DateFieldListFilter),)
