from django.db import models
from polymorphic.models import PolymorphicModel
from django.core.validators import RegexValidator


class Country(models.Model):
    iso_code_3 = models.CharField(max_length=3, validators=[RegexValidator(r'^\w{3}$', 'Must be exactly 3 characters')])


class Insured(models.Model):
    uuid = models.UUIDField()
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class ContractAdminInfo(models.Model):
    insured = models.ForeignKey(Insured, on_delete=models.CASCADE)


class Reinstatement(models.Model):
    premium_percentage = models.FloatField()


class ContractCoverageInfo(PolymorphicModel):
    policy_start_date = models.DateField()
    policy_end_date = models.DateField()
    participation = models.FloatField()


class ExcessOfLossEvent(ContractCoverageInfo):
    retention = models.FloatField()
    limit = models.FloatField(null=True)
    aggregate_retention = models.FloatField(null=True)
    reinstatements = models.ManyToManyField(Reinstatement)

    
class ExcessOfLossRisk(ContractCoverageInfo):
    retention = models.FloatField()
    limit = models.FloatField(null=True)
    aggregate_retention = models.FloatField(null=True)
    reinstatements = models.ManyToManyField(Reinstatement)


class QuotaShare(models.Model):
    share = models.FloatField(default=1)

    def __str__(self):
        return "Quota Share " + "{:.2f}%".format(self.share * 100)


def get_default_qs():
        return QuotaShare()

class Contract(models.Model):
    insured = models.CharField(max_length=256, default="default_insured")
    coverage_info = models.ForeignKey(QuotaShare, on_delete = models.CASCADE, default=get_default_qs)
