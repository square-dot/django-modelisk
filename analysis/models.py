from django.db import models
from django.db.models import Model, CharField, FloatField, DateField, JSONField
from django.db.models import ForeignKey, OneToOneField
from django.db.models import CASCADE
from django.urls import reverse

from insurance_contract.models import Program

class InflationPattern(Model):
    values = JSONField(default=dict)


class ExposureAnalysis(Model):
    name = CharField(max_length=256)
    inflation_pattern = ForeignKey(InflationPattern, on_delete = CASCADE)
    loss_distributions = JSONField(default=dict)
    program = ForeignKey(Program, on_delete=CASCADE)

    def code(self):
        return f"C{str(self.pk).zfill(5)}"
    
    def get_fields(self):
        return [("Code", self.code()),
                ("Name", self.name),
                ("Program", self.program),
                ]
    
    def get_absolute_url(self):
        return reverse("exposure-analysis-detail", args=[str(self.pk)])


class pareto_distribution():

    def __init__(self, threshold:float, alpha:float):
        self.threshold = threshold
        self.alpha = alpha

    def cdf(self, x):
        if x <= self.threshold:
            return 1
        return 1 - (self.threshold / x) ** self.alpha
    
    def pdf(self, x):
        if x <= self.threshold:
            return 0
        return self.alpha * (self.threshold ** self.alpha / (x ** (self.alpha + 1)))


