import numpy as np
import matplotlib.pyplot as plt

from yvain.membership_functions import Gaussian

if __name__ == '__main__':

    universe = np.linspace(0, 10, 1000)

    poor = Gaussian(0, 1.5)
    good = Gaussian(5, 1.5)
    excellent = Gaussian(10, 1.5)

    plt.plot(universe, [poor(x) for x in universe], label="poor")
    plt.plot(universe, [good(x) for x in universe], label="good")
    plt.plot(universe, [excellent(x) for x in universe], label="excellent")

    plt.legend()
    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")
    plt.title("Service")
