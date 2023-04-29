from django.core.management.base import BaseCommand
from analysis.synthetic_data.analysis_creation import CreateAnalysis

class Command(BaseCommand):
    help = 'Populate database with test-analysis'

    def handle(self, *args, **options):
        CreateAnalysis.depopulate_and_repopulate_test_analysis()
        self.stdout.write(self.style.SUCCESS('Successfully depopulated and populated the database with test analysis'))