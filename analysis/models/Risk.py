from django.db.models import Model, PROTECT, BooleanField, FloatField, ForeignKey, JSONField, CharField, PositiveIntegerField
from analysis.models.RiskProfile import RiskProfile


class Risk(Model):
    risk_profile = ForeignKey(RiskProfile, on_delete=PROTECT)
    name = CharField(max_length=256)
    quantity = PositiveIntegerField(default=1)
    expected_maximal_loss = FloatField()
    expected_average_loss = FloatField()
    tag_1 = CharField(max_length=256)
    tag_2 = CharField(max_length=256)
    tag_3 = CharField(max_length=256)