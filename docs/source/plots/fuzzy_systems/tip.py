import numpy as np
import matplotlib.pyplot as plt

from yvain.membership_functions import Triangle

if __name__ == '__main__':

    universe = np.linspace(0, 25, 1000)

    cheap = Triangle(0, 5, 10)
    average = Triangle(7.5, 12.5, 17.5)
    generous = Triangle(15, 20, 25)

    plt.plot(universe, [cheap(x) for x in universe], label="cheap")
    plt.plot(universe, [average(x) for x in universe], label="average")
    plt.plot(universe, [generous(x) for x in universe], label="generous")

    plt.legend()
    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")
    plt.title("Tip")
