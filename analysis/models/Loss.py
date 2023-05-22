from django.db.models import Model, PROTECT, FloatField, ForeignKey, CharField, PositiveIntegerField
from analysis.models.LossProfile import LossProfile


class Loss(Model):
    loss_profile = ForeignKey(LossProfile, on_delete=PROTECT)
    name = CharField(max_length=256)
    period = PositiveIntegerField(default=1)
    size = FloatField()
    importance = FloatField(default=1)

    def __str__(self):
        s = f"period: {self.period}, size: {self.size}, importance: {self.importance}"
        if self.name != "":
            return f"{self.name} {s}"
        return s