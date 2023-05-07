from analysis.models.ExposureAnalysis import ExposureAnalysis
from polymorphic.models import PolymorphicModel
from django.db.models import PROTECT, BooleanField, FloatField, ForeignKey, JSONField
from scipy.stats import pareto, gamma
import matplotlib.pyplot as plt


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
            self.type_string(), rounded_m, rounded_v, rounded_s, rounded_k
        )
    

class ParetoDistribution(LossDistribution):
    alpha = FloatField()
    threshold = FloatField()

    def type_string(self):
        return "Pareto"

    def cdf(self, x):
        return pareto.cdf(x, self.alpha, self.threshold)

    def ppf(self, x):
        return pareto.ppf(x, self.alpha, self.threshold)


class GammaDistribution(LossDistribution):
    shape = FloatField()
    rate = FloatField()

    def type_string(self):
        return "Gamma"

    def cdf(self, x):
        return gamma.cdf(x, self.shape, self.rate)

    def ppf(self, x):
        return gamma.ppf(x, self.shape, self.rate)


class EmpiricalDistribution(LossDistribution):
    sample = JSONField(null=True)

    def type_string(self):
        return "Empirical Distribution"

    def cdf(self, x):
        return NotImplementedError("ppf of ecdf still to define")

    def ppf(self, x):
        return NotImplementedError("ppf of ecdf still to define")

    def plot_and_save(self):
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Total distribution")

        # Save the plot as an image file
        image_path = "/analysis/plots/elephant.png"
        plt.savefig(image_path)
        plt.close()

        return image_path
