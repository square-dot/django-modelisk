from django.core.management.base import BaseCommand
from analysis.management.synthetic_data.analysis_creation import CreateAnalysis
from analysis.management.synthetic_data.data_creation import ContractsCreation
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Populate database with test-models'

    def handle(self, *args, **options):
        call_command("flush", verbosity=0, interactive=False)
        ContractsCreation.populate_test_data()
        CreateAnalysis.populate_test_analysis()

        self.stdout.write(self.style.SUCCESS('Successfully depopulated and repopulated the database'))