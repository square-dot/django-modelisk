from django.core.management.base import BaseCommand
from analysis.synthetic_data.analysis_creation import CreateAnalysis

class Command(BaseCommand):
    help = 'Populate database with test-analysis'

    def handle(self, *args, **options):
        CreateAnalysis.populate_test_analysis()
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test analysis'))

