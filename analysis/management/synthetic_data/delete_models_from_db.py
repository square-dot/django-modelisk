from analysis.models.reference_value.Code import Code
from analysis.models.reference_value.Company import Company
from analysis.models.contract.BaseContract import BaseContract
from analysis.models.contract.ExcessOfLossRisk import ExcessOfLossRisk
from analysis.models.contract.ExcessOfLossEvent import ExcessOfLossEvent
from analysis.models.contract.QuotaShare import QuotaShare
from analysis.models.reference_value.Country import Country
from analysis.models.reference_value.Currency import Currency
from analysis.models.ExposureAnalysis import ExposureAnalysis
from analysis.models.InflationPattern import InflationPattern
from analysis.models.LossDistribution import (
    EmpiricalDistribution,
    GammaDistribution,
    ParetoDistribution,
)
from analysis.models.contract.Premium import Premium
from analysis.models.contract.Program import Program
from analysis.models.contract.Reinstatement import Reinstatement


def empty_database_from_analysis():
    for c in (
        GammaDistribution,
        ParetoDistribution,
        EmpiricalDistribution,
        ExposureAnalysis,
        InflationPattern,
    ):
        c.objects.all().delete()


def empty_database():
    empty_database_from_analysis()
    for c in (
        ExposureAnalysis,
        InflationPattern,
        BaseContract,
        Program,
        QuotaShare,
        Reinstatement,
        ExcessOfLossRisk,
        ExcessOfLossEvent,
        Premium,
        Company,
        Code,
        Country,
        Currency,
    ):
        c.objects.all().delete()
