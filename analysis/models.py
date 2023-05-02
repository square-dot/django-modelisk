from django.db import models
from django.db.models import Model, CharField, FloatField, DateField, JSONField
from django.db.models import ForeignKey, OneToOneField
from django.db import models
from django.db.models import CASCADE
from polymorphic.models import PolymorphicModel
from django.core.validators import RegexValidator
from django.db.models.functions import Lower
from django.urls import reverse
from scipy.stats import gamma, pareto


class Country(Model):
    iso_code_3 = CharField(
        max_length=3,
        validators=[RegexValidator(r"^\w{3}$", "Must be exactly 3 characters")],
    )
    name = CharField(max_length=256, default="no_name")

    def __repr__(self) -> str:
        return self.iso_code_3

    def __str__(self) -> str:
        return self.__repr__()


class Currency(Model):
    iso_code_3 = CharField(
        max_length=3,
        validators=[RegexValidator(r"^\w{3}$", "Must be exactly 3 characters")],
    )
    name = CharField(max_length=256, default="no_name")

    def __repr__(self) -> str:
        return self.iso_code_3

    def __str__(self) -> str:
        return self.__repr__()


class Company(Model):
    name = CharField(max_length=256)
    country = ForeignKey(Country, on_delete=CASCADE)
    email = CharField(max_length=256, default="")

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_absolute_url(self):
        return reverse("company-detail", args=[str(self.pk)])

    def get_fields(self) -> list[tuple[str, str]]:
        return [
            ("Name", self.name),
            ("Country", self.country.name),
            ("E-mail", self.email),
        ]

    def get_fields_for_list(self) -> list[tuple[str, str, str]]:
        return [
            ("Name", self.get_absolute_url(), self.name),
            ("Country", "", self.country.name),
            ("E-mail", "", self.email),
        ]

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_lower_company_name")
        ]


class Reinstatements:
    def __init__(self, dict: dict[int, tuple[float, float]]):
        self.values = dict

    def add_reinstatement(self, size, cost) -> None:
        index = len(self.values) + 1
        self.values[index] = (size, cost)


class Coverage(PolymorphicModel):
    participation = FloatField(help_text="percentage share acquired")


class ExcessOfLoss(Coverage):
    risk_retention = FloatField(null=True, default=None)
    risk_limit = FloatField(null=True, default=None)
    event_retention = FloatField(null=True, default=None)
    event_limit = FloatField(null=True, default=None)
    aggregate_retention = FloatField(null=True, default=None)
    aggregate_limit = FloatField(null=True, default=None)
    reinstatements_data = JSONField(default=dict)

    def type_name(self) -> str:
        return "Excess Of Loss"

    def limit_retention_string(self) -> str:
        if self.risk_retention is not None:
            return "risk retention {:.0f}".format(self.risk_retention)
        return "no risk retention"

    def get_reinstatments(self) -> Reinstatements:
        reinstatments = Reinstatements({})
        for r in self.reinstatements_data:
            r.add_reinstatement(float(r.value[0]), float(r.value[0]))
        return reinstatments

    def __repr__(self):
        return self.type_name()

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str]]:
        l = []
        if self.risk_retention is not None:
            l.append(("Risk retention", "{:_}".format(self.risk_retention)))
        if self.risk_limit is not None:
            l.append(("Risk limit", "{:_}".format(self.risk_limit)))
        if self.event_retention is not None:
            l.append(("Event retention", "{:_}".format(self.event_retention)))
        if self.event_limit is not None:
            l.append(("Event limit", "{:_}".format(self.event_limit)))
        if self.aggregate_retention is not None:
            l.append(("Aggregate retention", "{:_}".format(self.aggregate_retention)))
        if self.aggregate_limit is not None:
            l.append(("Aggregate limit", "{:_}".format(self.aggregate_limit)))
        return l


class QuotaShare(Coverage):
    share = FloatField(default=1)

    def type_name(self) -> str:
        return "Quota Share"

    def __repr__(self):
        return self.type_name()

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str]]:
        return [("Share", "{:.0f}%".format(self.share * 100))]


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

    def get_absolute_url(self) -> str:
        return reverse("contract-detail", args=[str(self.pk)])

    def __repr__(self) -> str:
        return f"{self.code()} {self.coverage.__repr__()}"

    def __str__(self) -> str:
        return self.__repr__()

    def code(self) -> str:
        return f"C{str(self.pk).zfill(5)}"

    def get_fields(self) -> list[tuple[str, str]]:
        fields = [
            ("ID", self.code()),
            ("Type", self.coverage.type_name()),
            ("Premium", self.premium.upfront_premium),
            ("Brokerage", self.expenses.upfront_brokerage),
            ("Commission", self.expenses.upfront_commission),
        ]
        fields.extend(self.coverage.get_fields())
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        return [
            ("ID", self.get_absolute_url(), self.code()),
            ("Type", "", self.coverage.type_name()),
            ("Premium", "", self.premium.upfront_premium),
            ("Brokerage", "", self.expenses.upfront_brokerage),
            ("Commission", "", self.expenses.upfront_commission),
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
        return f"P{str(self.pk).zfill(5)}"

    def __repr__(self) -> str:
        return f"{self.code()} {self.insured}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_contracts(self) -> list[Contract]:
        contracts_pk = list(self.contracts.values())
        l = Contract.objects.filter(pk__in=contracts_pk)
        return list(l)

    def get_fields(self) -> list[tuple[str, str]]:
        contracts = [
            ("", f"{contract.code()} - {contract.coverage.type_name()}")
            for contract in self.get_contracts()
        ]

        fields = [
            ("ID", self.code()),
            ("Insured", self.insured),
            ("Start date", self.start_date),
            ("End date", self.end_date),
            ("Currency", self.currency),
            ("Contracts", len(self.contracts)),
        ]
        fields.extend(contracts)
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = [
            ("ID", self.get_absolute_url(), self.code()),
            ("Insured", self.insured.get_absolute_url(), self.insured),
            ("Start date", "", self.start_date),
            ("End date", "", self.end_date),
            ("Currency", "", self.currency),
            ("Nr of contracts", "", len(self.contracts)),
        ]
        return fields


class InflationPattern(Model):
    values = JSONField(default=dict)


class LossDistribution:
    TYPES = ("Gamma", "Pareto")

    def __init__(self, type: str, parameters: list[str]):
        self.distribution = gamma
        match type:
            case "Gamma":
                self.type = "Gamma"
                self.distribution = gamma
                self.parameters = [float(parameters[0]), float(parameters[1])]
            case "Pareto":
                self.type = "Pareto"
                self.distribution = pareto
                self.parameters = [float(parameters[0]), float(parameters[1])]
            case _:
                return ValueError("Type of distribution is unknown.")

    def cdf(self, x: float):
        self.distribution.cdf(
            x, self.parameters[0], loc=0, scale=1 / self.parameters[1]
        )

    def __str__(self):
        mean, var, skew, kurt = self.distribution.stats(
            self.parameters[0], moments="mvsk"
        )
        return f"{self.type}-mean:{mean}-variance:{var}-skewness:{skew}-kurtosis:{kurt}"


class ExposureAnalysis(Model):
    name = CharField(max_length=256)
    inflation_pattern = ForeignKey(InflationPattern, on_delete=CASCADE)
    loss_distributions_data = JSONField(default=dict)
    program = ForeignKey(Program, on_delete=CASCADE)

    def code(self):
        return f"C{str(self.pk).zfill(5)}"

    def get_fields(self):
        a = [
            ("Code", self.code()),
            ("Name", self.name),
            ("Program", self.program),
        ]
        for ld in self.get_distributions():
            a.append(("Distribution", ld))
        return a

    def get_distributions(self) -> list[LossDistribution]:
        a = []
        for _, value in self.loss_distributions_data.items():
            a.append(LossDistribution(value[0], value[1]))
        return a

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        return [
            ("Code", self.get_absolute_url(), self.code()),
            ("Name", "", self.name),
            ("Program", self.program.get_absolute_url(), self.program),
        ]

    def get_absolute_url(self):
        return reverse("exposure-analysis-detail", args=[str(self.pk)])
