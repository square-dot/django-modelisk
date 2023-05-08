from django.core.management.base import BaseCommand
from analysis.management.synthetic_data.delete_models_from_db import empty_database

class Command(BaseCommand):
    help = 'Empty db'

    def handle(self, *args, **options):
        empty_database()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all models'))