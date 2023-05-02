from analysis.models import (
    Country,
    Company,
    Premium,
    Expenses,
    Currency,
    Contract,
    QuotaShare,
    ExcessOfLoss,
    Program,
)
from analysis.models import ExposureAnalysis, InflationPattern


def empty_database():
    for c in (
        Country,
        Currency,
        Company,
        Premium,
        Expenses,
        Contract,
        QuotaShare,
        ExcessOfLoss,
        Program,
        ExposureAnalysis,
        InflationPattern,
    ):
        c.objects.all().delete()

def empty_database_from_analysis():
    for c in (
        ExposureAnalysis,
        InflationPattern,
    ):
        c.objects.all().delete()
