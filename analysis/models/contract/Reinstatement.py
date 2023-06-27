from analysis.models.contract.Layer import Layer
from django.db.models import CASCADE, FloatField, ForeignKey, Model, PositiveIntegerField


class Reinstatement(Model):
    contract = ForeignKey(Layer, on_delete=CASCADE)
    nr = PositiveIntegerField()
    size = FloatField(default=1)
    cost = FloatField(default=1)

    class Meta:
        unique_together = [('contract', 'nr')]