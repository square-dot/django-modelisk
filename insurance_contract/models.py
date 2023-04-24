from django.db import models
from polymorphic.models import PolymorphicModel
from django.core.validators import RegexValidator


class Country(models.Model):
    iso_code_3 = models.CharField(max_length=3, validators=[RegexValidator(r'^\w{3}$', 'Must be exactly 3 characters')])
    name = models.CharField(max_length=256)


class Insured(models.Model):
    name = models.CharField(max_length=256)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class AdministrativeInformation(models.Model):
    insured = models.ForeignKey(Insured, on_delete=models.CASCADE)


class ContractType(models.Model):
    TYPES = (("QS", "Quota Share"), ("XL_Risk", "Excess Of Loss Risk"), ("XL_Event", "Excess Of Loss Event"),)
    type = models.CharField(
        max_length=32,
        choices=TYPES,
        blank=True,
        default="QS",
        help_text="Type of contract",
    )


class Reinstatement(models.Model):
    premium_percentage = models.FloatField()


class Coverage(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    participation = models.FloatField(help_text="percentage share acquired")


class ExcessOfLoss(Coverage):
    risk_retention = models.FloatField()
    risk_limit = models.FloatField(null=True)
    event_retention = models.FloatField()
    event_limit = models.FloatField(null=True)
    aggregate_retention = models.FloatField()
    aggregate_limit = models.FloatField(null=True)
    reinstatements = models.ManyToManyField(Reinstatement)


class QuotaShare(Coverage):
    share = models.FloatField(default=1)

    def __str__(self):
        return "Quota Share " + "{:.2f}%".format(self.share * 100)


class Premium(models.Model):
    upfront_premium = models.FloatField()


class Expenses(models.Model):
    upfront_brokerage = models.FloatField()
    upfront_commission = models.FloatField()


class Contract(models.Model):
    administrative_information = models.ForeignKey(AdministrativeInformation, on_delete=models.CASCADE)
    premium = models.ForeignKey(Premium, on_delete=models.CASCADE)
    expenses = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    coverage = models.ForeignKey(Coverage, on_delete=models.PROTECT)
