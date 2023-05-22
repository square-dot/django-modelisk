from django.db.models import Model, PROTECT, FloatField, ForeignKey, CharField
from analysis.models.LossProfile import LossProfile


class Loss(Model):
    loss_profile = ForeignKey(LossProfile, on_delete=PROTECT)
    name = CharField(max_length=256)
    size = FloatField()
    importance = FloatField(default=1)