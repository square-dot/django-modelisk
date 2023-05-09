from analysis.models.LossDistribution import LossDistribution
import matplotlib.pyplot as plt
from modelisk.settings import BASE_DIR
import os
import math


def convolve(distributions: list[LossDistribution]) -> dict[int, float]:
    points = {i: math.sqrt(i) for i in range(1000)}
    return points


def plot_empirical_distribution(data_dict, anlysis_code):
    x = list(data_dict.values())
    y = [i / len(data_dict) for i in range(1, len(data_dict) + 1)]
    plt.show()
    plt.step(x, y, where="post")
    plt.xlabel("Observation")
    plt.ylabel("Cumulative Probability")
    plt.title("Empirical Distribution Function")
    file_path = os.path.join(
        BASE_DIR, "analysis/static/media/", f"plot_{anlysis_code}.png"
    )
    plt.savefig(file_path, format="png")
    return file_path
