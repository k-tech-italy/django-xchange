from contextlib import suppress

from django.contrib.auth.models import User
from django.core.management import BaseCommand, call_command
from django.db import IntegrityError

from django_xchange.models import Rate


class Command(BaseCommand):
    help = 'Setup Demo data'

    def handle(self, *args, **options):
        call_command('migrate')

        with suppress(IntegrityError):
            User.objects.create_superuser('admin', '', '123')

        Rate.objects.get_or_create(
            day='2022-01-01',
            defaults={'base': 'USD', 'rates': {'EUR': 0.863663, 'GBP': 0.751973, 'USD': 1}},
        )
