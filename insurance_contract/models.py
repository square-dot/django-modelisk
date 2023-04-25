from django.db import models
from polymorphic.models import PolymorphicModel
from django.core.validators import RegexValidator
from datetime import date
from django.db.models.functions import Lower
import random
from django.urls import reverse


class Country(models.Model):
    iso_code_3 = models.CharField(max_length=3, validators=[RegexValidator(r'^\w{3}$', 'Must be exactly 3 characters')])
    name = models.CharField(max_length=256, default="no_name")

    def __repr__(self) -> str:
        return self.iso_code_3
    
    def __str__(self) -> str:
        return self.__repr__()


class Company(models.Model):
    name = models.CharField(max_length=256)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"{self.name}, [{self.country}]"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def get_absolute_url(self):
        return reverse("company-detail", args=[str(self.pk)])
    
    class Meta:
        constraints = [ models.UniqueConstraint(Lower("name"), name="unique_lower_company_name")]


class AdministrativeInformation(models.Model):
    name = models.CharField(max_length=256, default="no name")
    insured = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return self.insured.__repr__()

    def __str__(self) -> str:
        return self.__repr__()


class ContractType():
    TYPES = (("QS", "Quota Share"), ("XL_Risk", "Excess Of Loss Risk"), ("XL_Event", "Excess Of Loss Event"),)

    def __init__(self, type_string):
        if type_string in [t[0] for t in self.TYPES]:
            self.type = type_string
        else:
            return ValueError(f"{type_string} is not a valid contract type")
        
    def __str__(self):
        return next(t[1] for t in self.TYPES if t[0] == self.type)
    
    def is_quota_share(self):
        return self.type == "QS"
    
    def is_excess_of_loss(self):
        return self.type == "XL_Risk" or self.type == "XL_Event"


class Reinstatement(models.Model):
    premium_percentage = models.FloatField()


class Coverage(PolymorphicModel):
    start_date = models.DateField()
    end_date = models.DateField()
    participation = models.FloatField(help_text="percentage share acquired")

    def __repr__(self) -> str:
        return "should return subclass"

    def __str__(self) -> str:
        return self.__repr__()
    
    def start_end_date(self):
        return f"{self.start_date} - {self.end_date}"
    
    def type_name(self):
        return NotImplementedError


class ExcessOfLoss(Coverage):
    risk_retention = models.FloatField(null=True)
    risk_limit = models.FloatField(null=True)
    event_retention = models.FloatField(null=True)
    event_limit = models.FloatField(null=True)
    aggregate_retention = models.FloatField(null=True)
    aggregate_limit = models.FloatField(null=True)
    reinstatements = models.ManyToManyField(Reinstatement)

    def type_name(self):
        return "Excess Of Loss"
    
    def limit_retention_string(self):
        if self.risk_retention is not None:
            return "risk retention {:.0f}".format(self.risk_retention)
        return "no risk retention"

        
    def __repr__(self):
        return self.type_name() + self.limit_retention_string()

    def __str__(self) -> str:
        return self.__repr__()

class QuotaShare(Coverage):
    share = models.FloatField(default=1)

    def type_name(self):
        return "Quota Share"

    def __repr__(self):
        return self.type_name() + " {:.0f}%".format(self.share * 100)
    
    def __str__(self) -> str:
        return self.__repr__()


class Premium(models.Model):
    upfront_premium = models.FloatField()


class Expenses(models.Model):
    upfront_brokerage = models.FloatField()
    upfront_commission = models.FloatField()

    @staticmethod
    def default():
        e = Expenses(upfront_commission=0, upfront_brokerage=0)
        e.save()


class Contract(models.Model):
    administrative_information = models.OneToOneField(AdministrativeInformation, on_delete=models.CASCADE)
    premium = models.OneToOneField(Premium, on_delete=models.CASCADE)
    expenses = models.OneToOneField(Expenses, on_delete=models.CASCADE)
    coverage = models.OneToOneField(Coverage, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("contract-detail", args=[str(self.pk)])

    @staticmethod
    def default_name(coverage, insured_name:str):
        return f"{coverage.type_name()} - " + insured_name

    def __repr__(self) -> str:
        return self.administrative_information.__repr__() + " " + self.coverage.__repr__()
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def name(self):
        return self.administrative_information.name
    
    def start_date(self):
        return self.coverage.start_date
    
    def end_date(self):
        return self.coverage.end_date
    
    def insured(self):
        return self.administrative_information.insured
