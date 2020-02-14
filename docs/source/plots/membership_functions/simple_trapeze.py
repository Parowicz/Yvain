from math import isclose

import numpy as np

from docs.source.plots.membership_functions.membership_plot import draw_mf
from yvain.membership_functions import Trapezoid
import matplotlib.pyplot as plt

if __name__ == '__main__':
    a, b, c, d = 1, 3, 7, 9
    universe_start, universe_end = 0, 10
    universe = np.linspace(universe_start, universe_end, 1000)
    mf = Trapezoid(a=1, b=3, c=7, d=9)

    draw_mf(mf, universe_start, universe_end,
            f"Trapezoid(a={a}, b={b}, c={c}, d={d})")
    plt.fill_between(universe, [mf(x) if isclose(mf(x), 1) else 0 for x in universe],
                     alpha=0.4, color="grey")
    plt.vlines([b, c], ymin=0, ymax=1, colors="gray",
               linestyles="--")
