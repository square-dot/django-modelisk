import os

import matplotlib.pyplot as plt

from analysis.models.ProbabilityDistribution import EmpiricalDistribution
from modelisk.settings import BASE_DIR


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


def name_of_total_distribution_plot(ecdf: EmpiricalDistribution):
    assert ecdf.is_total_distribution
    return f"plot_{ecdf.contract.code}.png"


def plot_folder() -> str:
    file_path = os.path.join(BASE_DIR, "analysis/static/media/")
    return file_path
