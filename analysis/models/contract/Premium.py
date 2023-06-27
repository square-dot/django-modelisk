from django.db.models import FloatField, Model


class Premium(Model):
    upfront_premium = FloatField()
    swing_rate = FloatField(null = True, default=None)
    no_claim_bonus = FloatField(null = True, default=None)
    
