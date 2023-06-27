from typing import Any
from django.db.models import Model, CASCADE, ForeignKey, OneToOneField, CharField
from analysis.models.RiskProfile import RiskProfile

class RiskProfileModel(Model):
    risk_profile = ForeignKey(RiskProfile, on_delete=CASCADE)