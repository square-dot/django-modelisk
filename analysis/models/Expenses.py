from django.db.models import FloatField, Model


class Expenses(Model):
    upfront_brokerage = FloatField()
    upfront_commission = FloatField()

    @staticmethod
    def default():
        e = Expenses(upfront_commission=0, upfront_brokerage=0)
        e.save()