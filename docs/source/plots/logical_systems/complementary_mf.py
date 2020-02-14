import matplotlib.pyplot as plt
import numpy as np

from yvain.logical_systems import Zadeh
from yvain.membership_functions import Gaussian

if __name__ == '__main__':
    mf = Gaussian(4.5, 1)

    logic = Zadeh()
    mf_negated = logic.complement(mf)

    universe = np.linspace(0, 10, 1000)
    plt.plot(universe, [mf(x) for x in universe], label="gaussian mf")
    plt.plot(universe, [mf_negated(x) for x in universe], "--", label="complementary mf")

    plt.xlabel("x")
    plt.ylabel(r"$\mu$(x)")
    plt.legend()
