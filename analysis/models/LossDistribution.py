from analysis.models.ExposureAnalysis import ExposureAnalysis
from django.db.models import PROTECT, BooleanField, CharField, ForeignKey, Model


class LossDistribution(Model):
    GAMMA = "gamma"
    PARETO = "pareto"
    ECDF = "ecdf"
    TYPE_CHOICES = ((GAMMA, "gamma"), (PARETO, "pareto"), (ECDF, "ecdf"))
    analysis = ForeignKey(ExposureAnalysis, on_delete=PROTECT)
    is_total_distribution = BooleanField(default=False)
    type = CharField(max_length=16, choices=TYPE_CHOICES, default=GAMMA)

    def __str__(self):
        # mean, var, skew, kurt = self.distribution.stats(
        #     self.parameters[0], moments="mvsk"
        # )
        mean, var, skew, kurt = 1, 2, 4, 8
        rounded_m = "{:,.2f}".format(mean).replace(",", "_")
        rounded_v = "{:,.2f}".format(var).replace(",", "_")
        rounded_s = "{:,.2f}".format(skew).replace(",", "_")
        rounded_k = "{:,.2f}".format(kurt).replace(",", "_")
        return "{}-mean:{}-variance:{}-skewness:{}-kurtosis:{}".format(
            self.type, rounded_m, rounded_v, rounded_s, rounded_k
        )
