from django.core.management.base import BaseCommand
from analysis.management.synthetic_data.analysis_creation import CreateAnalysis
from analysis.management.synthetic_data.data_creation import ContractsCreation
from analysis.management.synthetic_data.delete_models_from_db import empty_database

class Command(BaseCommand):
    help = 'Populate database with test-models'

    def handle(self, *args, **options):
        empty_database()
        ContractsCreation.populate_test_data()
        CreateAnalysis.populate_test_analysis()

        self.stdout.write(self.style.SUCCESS('Successfully depopulated and repopulated the database'))