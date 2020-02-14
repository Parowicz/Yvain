from docs.source.plots.membership_functions.membership_plot import draw_mf
from yvain.membership_functions import Sigmoid
import matplotlib.pyplot as plt
import numpy as np


def draw_sigmoid(a, b):
    universe = np.linspace(0, 10, 1000)
    mf = Sigmoid(a, b)

    plt.plot(universe, [mf(x) for x in universe], label=f"sigmoid({a}, {b})")

    plt.vlines(a, ymin=0, ymax=1, color="grey", linestyles="--")

    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")


if __name__ == '__main__':
    draw_mf(Sigmoid(5, 2), 0, 10,
            "Sigmoid(a=5, b=2)", False)
    draw_mf(Sigmoid(5, -2), 0, 10,
            "Sigmoid(a=5, b=-2)", False)
    plt.vlines(5, ymin=0, ymax=1, colors="gray",
               linestyles="--")
