from django.db.models import JSONField, Model


class InflationPattern(Model):
    values = JSONField(default=dict)