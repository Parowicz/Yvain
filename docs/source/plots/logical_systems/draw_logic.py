import matplotlib.pyplot as plt
import numpy as np

from yvain.membership_functions import Triangle, Gaussian


def draw_system(logic, title):
    mf1 = Triangle(0, 3, 6)
    mf2 = Gaussian(4.5, 1)
    mf3 = Triangle(3, 6, 9)

    mf1_or2_or3 = logic.t_conorm(logic.t_conorm(mf1, mf2), mf3)
    mf1_and2_and3 = logic.t_norm(logic.t_norm(mf1, mf2), mf3)

    universe = np.linspace(0, 10, 1000)

    plt.plot(universe, [mf1(x) for x in universe], "--")
    plt.plot(universe, [mf2(x) for x in universe], "--")
    plt.plot(universe, [mf3(x) for x in universe], "--")
    plt.plot(universe, [mf1_or2_or3(x) for x in universe], label="T-Conorm")
    plt.plot(universe, [mf1_and2_and3(x) for x in universe], label="T-Norm")

    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")
    plt.title(title)
    plt.legend()
