from django.core.management.base import BaseCommand
from analysis.management.synthetic_data.analysis_creation import CreateAnalysis
from analysis.management.synthetic_data.delete_models_from_db import empty_database_from_analysis

class Command(BaseCommand):
    help = 'Repopulate database with test-analysis'

    def handle(self, *args, **options):
        empty_database_from_analysis()
        CreateAnalysis.populate_test_analysis()

        self.stdout.write(self.style.SUCCESS('Successfully depopulated and repopulated the database with new analysis'))