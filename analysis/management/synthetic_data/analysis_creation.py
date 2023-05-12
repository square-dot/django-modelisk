from analysis.models.InflationPattern import InflationPattern
from analysis.models.contract.Program import Program
from analysis.models.LossDistribution import ParetoDistribution, GammaDistribution
from analysis.models.ExposureAnalysis import ExposureAnalysis
import random


class CreateAnalysis:
    @staticmethod
    def populate_test_analysis():
        programs = list(Program.objects.all()) # type: ignore
        inflation = InflationPattern.objects.create()
        analysis = CreateAnalysis.create_test_analysis(programs, inflation)
        CreateAnalysis.create_loss_distributions(analysis)

    @staticmethod
    def depopulate_and_repopulate_test_analysis():
        CreateAnalysis.populate_test_analysis()

    @staticmethod
    def create_loss_distributions(analysis: list[ExposureAnalysis]):
        for i, a in enumerate(analysis):
            match i % 2:
                case 0:
                    ParetoDistribution.objects.create(
                        analysis=a,
                        is_total_distribution=False,
                        alpha = 2,
                        threshold = 10_000,
                    )
                case 1:
                    GammaDistribution.objects.create(
                        analysis=a,
                        is_total_distribution=False,
                        shape = 2,
                        rate = 0.01
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
