from analysis.models.ExcessOfLoss import ExcessOfLoss
from django.db.models import PROTECT, FloatField, ForeignKey, Model, PositiveIntegerField


class Reinstatement(Model):
    coverage = ForeignKey(ExcessOfLoss, on_delete=PROTECT)
    nr = PositiveIntegerField()
    size = FloatField(default=1)
    cost = FloatField(default=1)

    class Meta:
        unique_together = [('coverage', 'nr')]