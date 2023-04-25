from django.core.management.base import BaseCommand
from insurance_contract.syntethic_data import ContractsCreation

class Command(BaseCommand):
    help = 'Depopulate and repopulate test data in the database'

    def handle(self, *args, **options):
        ContractsCreation.depopulate_and_repopulate_test_data()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all values and repopulated test data'))