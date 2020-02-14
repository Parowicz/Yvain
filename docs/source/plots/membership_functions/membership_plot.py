from math import isclose
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt


def draw_mf(mf: Callable[[float, ], float], start: float, end: float,
            title: str):
    universe = np.linspace(start, end, 1000)

    plt.plot(universe, [mf(x) for x in universe])

    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")
    plt.title(title)
