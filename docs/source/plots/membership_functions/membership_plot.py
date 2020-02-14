from math import isclose
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt


def draw_mf(mf: Callable[[float, ], float], start: float, end: float,
            title: str, draw_absolute_membership: bool = True):
    universe = np.linspace(start, end, 1000)

    plt.plot(universe, [mf(x) for x in universe])

    if draw_absolute_membership:
        plt.fill_between(universe, [mf(x) if isclose(mf(x), 1) else 0 for x in universe],
                         alpha=0.4, color="grey")

    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")
    plt.title(title)
