from django.core.management.base import BaseCommand
from insurance_contract.syntethic_data import ContractsCreation

class Command(BaseCommand):
    help = 'Delete all data from the database'

    def handle(self, *args, **options):
        ContractsCreation.empty_database()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all values from the db'))