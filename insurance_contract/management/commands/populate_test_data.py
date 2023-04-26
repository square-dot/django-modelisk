from django.core.management.base import BaseCommand
from insurance_contract.synthetic_data.data_creation import ContractsCreation

class Command(BaseCommand):
    help = 'Populate test data in the database'

    def handle(self, *args, **options):
        ContractsCreation.populate_test_data()
        self.stdout.write(self.style.SUCCESS('Successfully populated test data'))
