from docs.source.plots.membership_functions.membership_plot import draw_mf
from yvain.membership_functions import Triangle
import matplotlib.pyplot as plt

if __name__ == '__main__':
    a, b, c = 2, 5, 8
    draw_mf(Triangle(a=a, b=b, c=c), 0, 10,
            f"Triangle(a={a}, b={b}, c={c})", False)
    plt.vlines(b, ymin=0, ymax=1, colors="gray",
               linestyles="--")
