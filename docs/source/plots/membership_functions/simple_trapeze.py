from docs.source.plots.membership_functions.membership_plot import draw_mf
from yvain.membership_functions import Trapezoid
import matplotlib.pyplot as plt

if __name__ == '__main__':
    a, b, c, d = 1, 3, 7, 9
    draw_mf(Trapezoid(a=1, b=3, c=7, d=9), 0, 10,
            f"Trapezoid(a={a}, b={b}, c={c}, d={d})")
    plt.vlines([b, c], ymin=0, ymax=1, colors="gray",
               linestyles="--")
