import math

from analysis.models.ProbabilityDistribution import ProbabilityDistribution

# from scipy.fft import ff


def convolve_all(distributions: list[ProbabilityDistribution]): #-> dict[int, float]:
    first = distributions[0]
    conv = []
    for d in distributions[1:]:
        pass


# def convolve(d1, d2):
#     l1 = d1.ppf(0.999)
#     l2 = d2.ppf(0.999)
#     pp1 = [p for p in range(0, l1*2, l1*2/10_000)]
#     pp2 = [p for p in range(0, l2*2, l2*2/10_000)]
