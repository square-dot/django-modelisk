from analysis.models import ExposureAnalysis, InflationPattern
from insurance_contract.models import Program
import random


class CreateAnalysis:
    @staticmethod
    def populate_test_analysis():
        programs = list(Program.objects.all())
        inflation = InflationPattern.objects.create(values={})
        CreateAnalysis.create_test_analysis(programs, inflation)

    @staticmethod
    def depopulate_and_repopulate_test_analysis():
        CreateAnalysis.empty_database()
        CreateAnalysis.populate_test_analysis()

    @staticmethod
    def create_test_analysis(programs:list[Program], inflation:InflationPattern):
        nr = 50
        for _ in range(nr):
            ExposureAnalysis.objects.create(
                name="Test analysis",
                inflation_pattern=inflation,
                loss_distributions={},
                program=random.choice(programs),
            )

    @staticmethod
    def empty_database():
        for c in (
            ExposureAnalysis,
            InflationPattern,
        ):
            c.objects.all().delete()
