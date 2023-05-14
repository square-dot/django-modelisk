from django.db.models import Model, PROTECT, BooleanField, FloatField, ForeignKey, JSONField, CharField, PositiveIntegerField

class RiskProfile(Model):
    name = CharField(max_length=256)