
from django.core.management.base import BaseCommand

from ... import generating


class Command(BaseCommand):

    def handle(self, *args, **options):
        generating.generate()
