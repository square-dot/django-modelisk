from analysis.models.ExposureAnalysis import ExposureAnalysis
from analysis.models.InflationPattern import InflationPattern
from analysis.models.ProbabilityDistribution import (
    EmpiricalDistribution,
    GammaDistribution,
    ParetoDistribution,
)


def empty_database_from_analysis():
    for c in (
        GammaDistribution,
        ParetoDistribution,
        EmpiricalDistribution,
        ExposureAnalysis,
        InflationPattern,
    ):
        c.objects.all().delete()
