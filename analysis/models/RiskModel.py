from typing import Any
from django.db.models import Model, CASCADE, PROTECT, ForeignKey, OneToOneField, CharField
from analysis.models.RiskProfileModel import RiskProfileModel
from analysis.models.ProbabilityDistribution import ProbabilityDistribution

class RiskModel(Model):
    risk_profile_model = ForeignKey(RiskProfileModel, on_delete=CASCADE)
    probability_distribution = OneToOneField(ProbabilityDistribution, on_delete=PROTECT)
    tags_string = CharField(max_length=1024)

    def tags(self) -> list[str]:
        return self.tags_string.split(" ")