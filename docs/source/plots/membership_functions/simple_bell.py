from docs.source.plots.membership_functions.membership_plot import draw_mf
from yvain.membership_functions import Bell
import matplotlib.pyplot as plt

if __name__ == '__main__':
    mu, sigma, gamma = 5, 2, 2
    draw_mf(Bell(mu=mu, sigma=sigma, gamma=gamma), 0, 10,
            f"Bell(mu={mu}, sigma={sigma}, gamma={gamma})")
    plt.vlines(mu, ymin=0, ymax=1, colors="gray",
               linestyles="--")
