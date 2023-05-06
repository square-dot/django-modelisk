from analysis.models.LossDistribution import LossDistribution


def convolve(distributions:list[LossDistribution]) -> list[float]:
    return [0.01 * i for i in range(100)]