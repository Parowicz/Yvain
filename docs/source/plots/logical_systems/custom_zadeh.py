from docs.source.examples.custom_zadeh import MyZadeh
from docs.source.plots.logical_systems.draw_logic import draw_system


if __name__ == '__main__':
    draw_system(MyZadeh(), "Custom Zadeh")
