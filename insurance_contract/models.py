from django.db import models
from django.db.models import Model, CharField, FloatField, DateField, JSONField
from django.db.models import ForeignKey, OneToOneField
from django.db.models import CASCADE
from polymorphic.models import PolymorphicModel
from django.core.validators import RegexValidator
from django.db.models.functions import Lower
from django.urls import reverse

class Country(Model):
    iso_code_3 = CharField(max_length=3, validators=[RegexValidator(r'^\w{3}$', 'Must be exactly 3 characters')])
    name = CharField(max_length=256, default="no_name")

    def __repr__(self) -> str:
        return self.iso_code_3
    
    def __str__(self) -> str:
        return self.__repr__()
    
class Currency(Model):
    iso_code_3 = CharField(max_length=3, validators=[RegexValidator(r'^\w{3}$', 'Must be exactly 3 characters')])
    name = CharField(max_length=256, default="no_name")

    def __repr__(self) -> str:
        return self.iso_code_3
    
    def __str__(self) -> str:
        return self.__repr__()


class Company(Model):
    name = CharField(max_length=256)
    country = ForeignKey(Country, on_delete=CASCADE)

    def __repr__(self) -> str:
        return f"{self.name}, [{self.country}]"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def get_absolute_url(self):
        return reverse("company-detail", args=[str(self.pk)])
    
    def get_fields(self):
        return [("Name", self.name), ("Country", self.country.name)]
    
    class Meta:
        constraints = [ models.UniqueConstraint(Lower("name"), name="unique_lower_company_name")]


class Reinstatements():
    
    def __init__(self):
        self.values = {}

    def add_reinstatement(self, size, cost):
        index = len(self.values) + 1
        self.values[index] = (size, cost)


class Coverage(PolymorphicModel):
    participation = FloatField(help_text="percentage share acquired")

    def __repr__(self) -> str:
        return "should return subclass"

    def __str__(self) -> str:
        return self.__repr__()
    
    def type_name(self):
        return NotImplementedError


class ExcessOfLoss(Coverage):
    risk_retention = FloatField(null=True)
    risk_limit = FloatField(null=True)
    event_retention = FloatField(null=True)
    event_limit = FloatField(null=True)
    aggregate_retention = FloatField(null=True)
    aggregate_limit = FloatField(null=True)
    reinstatements = JSONField()

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
    share = FloatField(default=1)

    def type_name(self):
        return "Quota Share"

    def __repr__(self):
        return self.type_name() + " {:.0f}%".format(self.share * 100)
    
    def __str__(self) -> str:
        return self.__repr__()


class Premium(Model):
    upfront_premium = FloatField()


class Expenses(Model):
    upfront_brokerage = FloatField()
    upfront_commission = FloatField()

    @staticmethod
    def default():
        e = Expenses(upfront_commission=0, upfront_brokerage=0)
        e.save()


class Contract(Model):
    currency = ForeignKey(Currency, on_delete=CASCADE)
    premium = OneToOneField(Premium, on_delete=CASCADE)
    expenses = OneToOneField(Expenses, on_delete=CASCADE)
    coverage = OneToOneField(Coverage, on_delete=CASCADE)

    def get_absolute_url(self):
        return reverse("contract-detail", args=[str(self.pk)])

    def __repr__(self) -> str:
        return f"{self.code()} {self.coverage.__repr__()}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def code(self):
        return f"CN-{str(self.pk).zfill(5)}"
    
    
    def get_fields(self):
        return [("ID", self.code()),
                ("Type", self.coverage.type_name()),
                ("Premium", self.premium.upfront_premium),
                ("Brokerage", self.expenses.upfront_brokerage),
                ("Commission", self.expenses.upfront_commission),
                ]

class Program(Model):
    insured = ForeignKey(Company, on_delete=CASCADE)
    currency = ForeignKey(Currency, on_delete=CASCADE)
    start_date = DateField()
    end_date = DateField()
    contracts = JSONField()

    def get_absolute_url(self):
        return reverse("program-detail", args=[str(self.pk)])

    def code(self):
        return f"PN-{str(self.pk).zfill(4)}"
    
    def get_contracts(self) -> list[Contract]:
        contracts_pk = list(self.contracts.values())
        l = Contract.objects.filter(pk__in=contracts_pk)
        return list(l)

    def get_fields(self) -> list:
        contracts = [("", f"{contract.code()} - {contract.coverage.type_name()}") for contract in self.get_contracts()]

        fields = [("ID", self.code()),
                ("Insured", self.insured),
                ("Start date", self.start_date),
                ("End date", self.end_date),
                ("Currency", self.currency),
                ("# contracts", len(self.contracts)),
                ]
        fields.extend(contracts)
        return fields