import numpy as np
import matplotlib.pyplot as plt

from yvain.membership_functions import Trapezoid

if __name__ == '__main__':

    universe = np.linspace(0, 10, 1000)

    rancid = Trapezoid(-2, 0, 2, 4)
    delicious = Trapezoid(7, 9, 11, 13)

    plt.plot(universe, [rancid(x) for x in universe], label="rancid")
    plt.plot(universe, [delicious(x) for x in universe], label="delicious")

    plt.legend()
    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")
    plt.title("Food")
