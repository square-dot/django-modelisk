from django.core.management.base import BaseCommand
from analysis.synthetic_data.analysis_creation import CreateAnalysis

class Command(BaseCommand):
    help = 'Delete all analysis from the database'

    def handle(self, *args, **options):
        CreateAnalysis.empty_database()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all values from the db'))