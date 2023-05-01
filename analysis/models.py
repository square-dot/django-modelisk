from django.db import models
from django.db.models import Model, CharField, FloatField, DateField, JSONField
from django.db.models import ForeignKey, OneToOneField
from django.db.models import CASCADE
from django.urls import reverse
from scipy.stats import gamma, pareto


from insurance_contract.models import Program


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
