from django.db import models
from django.db.models import Model, CharField, FloatField, DateField, JSONField
from django.db.models import ForeignKey, OneToOneField
from django.db.models import CASCADE

from insurance_contract.models import Program

class InflationPattern(models.Model):
    values = models.JSONField("values")


class ExposureAnalysis(Model):
    name = CharField(max_length=256)
    inflation_pattern = ForeignKey(InflationPattern, on_delete = CASCADE)
    loss_distributions = JSONField()
    program = ForeignKey(Program, on_delete=CASCADE)


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


