from analysis.models.Company import Company
from analysis.models.Contract import Contract
from analysis.models.Country import Country
from analysis.models.Currency import Currency
from analysis.models.ExcessOfLoss import ExcessOfLoss
from analysis.models.Expenses import Expenses
from analysis.models.InflationPattern import InflationPattern
from analysis.models.Premium import Premium
from analysis.models.QuotaShare import QuotaShare
from analysis.models.Program import Program
from analysis.models.Code import Code
from analysis.models.ExposureAnalysis import ExposureAnalysis
from analysis.models.Reinstatement import Reinstatement


def empty_database():
    for c in (
        ExposureAnalysis,
        InflationPattern,
        Contract,
        Program,
        QuotaShare,
        ExcessOfLoss,
        Reinstatement,
        Premium,
        Expenses,
        Company,
        Code,
        Country,
        Currency,
    ):
        c.objects.all().delete()


def empty_database_from_analysis():
    for c in (
        ExposureAnalysis,
        InflationPattern,
    ):
        c.objects.all().delete()
