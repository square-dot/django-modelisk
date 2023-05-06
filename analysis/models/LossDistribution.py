from analysis.models.ExposureAnalysis import ExposureAnalysis
from polymorphic.models import PolymorphicModel
from django.db.models import PROTECT, BooleanField, FloatField, ForeignKey, JSONField
from scipy.stats import pareto, gamma, ecdf


class LossDistribution(PolymorphicModel):
    GAMMA = "gamma"
    PARETO = "pareto"
    ECDF = "ecdf"
    TYPE_CHOICES = ((GAMMA, "gamma"), (PARETO, "pareto"), (ECDF, "ecdf"))

    analysis = ForeignKey(ExposureAnalysis, on_delete=PROTECT)
    is_total_distribution = BooleanField(default=False)


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


class ParetoDistribution(LossDistribution):
    alpha = FloatField()
    threshold = FloatField()
    
    def cdf(self, x):
        return pareto.cdf(x, self.alpha, self.threshold)

    def ppf(self, x):
        return pareto.ppf(x, self.alpha, self.threshold)


class GammaDistribution(LossDistribution):
    shape = FloatField()
    rate = FloatField()
    
    def cdf(self, x):
        return gamma.cdf(x, self.shape, self.rate)

    def ppf(self, x):
        return gamma.ppf(x, self.shape, self.rate)


class EmpiricalDistribution(LossDistribution):
    sample = JSONField()


    def cdf(self, x):
        ecdf = ecdf(self.sample)
        return ecdf.evaluate(x)

    def ppf(self, x):
        ecdf = ecdf(self.sample)
        return NotImplementedError("ppf of ecdf still to define")
