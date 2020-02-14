from docs.source.plots.membership_functions.membership_plot import draw_mf
from yvain.membership_functions import Sigmoid
import matplotlib.pyplot as plt

if __name__ == '__main__':
    draw_mf(Sigmoid(5, 2), 0, 10, "Sigmoid(a=5, b=2)")
    draw_mf(Sigmoid(5, -2), 0, 10, "Sigmoid(a=5, b=-2)")
    plt.vlines(5, ymin=0, ymax=1, colors="gray", linestyles="--")
