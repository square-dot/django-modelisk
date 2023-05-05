from django.db.models import FloatField, Model


class Premium(Model):
    upfront_premium = FloatField()
