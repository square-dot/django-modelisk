from django.db.models import FloatField, Model

class Expenses(Model):
    upfront_expenses = FloatField(default=0)
    reinstatement_expenses = FloatField(default=0)
    loss_based_expenses = FloatField(default=0)
    upfront_commission = FloatField(default=0)
    sliding_scale_commission = FloatField(default=0)
