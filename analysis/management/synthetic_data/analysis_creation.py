from analysis.models.InflationPattern import InflationPattern
from analysis.models.Program import Program
from analysis.models.Premium import LossDistribution
from analysis.models.ExposureAnalysis import ExposureAnalysis
import random


class CreateAnalysis:
    @staticmethod
    def populate_test_analysis():
        programs = list(Program.objects.all())
        inflation = InflationPattern.objects.create(values={})
        analysis = CreateAnalysis.create_test_analysis(programs, inflation)
        CreateAnalysis.create_loss_distributions(analysis)

    @staticmethod
    def depopulate_and_repopulate_test_analysis():
        CreateAnalysis.populate_test_analysis()

    @staticmethod
    def create_loss_distributions(analysis: list[ExposureAnalysis]):
        for a in analysis:
            LossDistribution.objects.create(
                analysis=a,
                is_total_distribution=False,
                type=random.choice(
                    (
                        LossDistribution.GAMMA,
                        LossDistribution.PARETO,
                        LossDistribution.ECDF,
                    )
                ),
            )

    @staticmethod
    def create_test_analysis(programs: list[Program], inflation: InflationPattern):
        nr = 50
        for _ in range(nr):
            ExposureAnalysis.objects.create(
                name="Test analysis",
                inflation_pattern=inflation,
                program=random.choice(programs),
            )
        return list(ExposureAnalysis.objects.all())
