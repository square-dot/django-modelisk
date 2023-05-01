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
        CreateAnalysis.populate_test_analysis()

    @staticmethod
    def create_test_analysis(programs: list[Program], inflation: InflationPattern):
        nr = 50
        for _ in range(nr):
            ExposureAnalysis.objects.create(
                name="Test analysis",
                inflation_pattern=inflation,
                loss_distributions_data={
                    "1": ("Gamma", ("5", "1")),
                    "2": ("Pareto", ("5", "100")),
                },
                program=random.choice(programs),
            )
