from docs.source.plots.logical_systems.draw_logic import draw_system
from yvain.logical_systems import Dombi

if __name__ == '__main__':
    draw_system(Dombi(0.1), "Dombi system with $p = 0.1$")
