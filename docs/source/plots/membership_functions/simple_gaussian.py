from docs.source.plots.membership_functions.membership_plot import draw_mf
from yvain.membership_functions import Gaussian
import matplotlib.pyplot as plt

if __name__ == '__main__':
    mu, sigma = 5, 2
    draw_mf(Gaussian(mu=5, sigma=2), 0, 10,
            f"Gaussian(mu={mu}, sigma={sigma})", False)
    plt.vlines(mu, ymin=0, ymax=1, colors="gray",
               linestyles="--")
