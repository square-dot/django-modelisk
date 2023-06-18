import math

from analysis.models.ProbabilityDistribution import ProbabilityDistribution, EmpiricalDistribution

from scipy.signal import fftconvolve


def convolve_all(distributions: list[ProbabilityDistribution]) -> dict[int, float]:
    first = distributions[0]
    convolution = first
    for d in distributions[1:]:
        plan = ConvolutionPlan(convolution, d)
        convolution = convolve(convolution, d, plan)
    return convolution

class ConvolutionPlan:

    def __init__(self, d1:ProbabilityDistribution, d2:ProbabilityDistribution):
        self.sart_at = 0
        d1_max = d1.ppf(0.999)
        d2_max = d2.ppf(0.999)
        self.end_at = max(d1_max, d2_max)
        self.points = range(self.sart_at, self.end_at, (self.end_at - self.sart_at) / 10_000)


def convolve(d1:ProbabilityDistribution, d2:ProbabilityDistribution, plan:ConvolutionPlan) -> ProbabilityDistribution:
    pp1 = [d1.cdf(plan.points[i]) - d1.cdf(plan.points[i + 1]) for i in range(0, len(plan.points) - 1)]
    pp2 = [d2.cdf(plan.points[i]) - d2.cdf(plan.points[i + 1]) for i in range(0, len(plan.points) - 1)]
    convolution = fftconvolve(pp1, pp2)
    return EmpiricalDistribution(sample = convolution)




