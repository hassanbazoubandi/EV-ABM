import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes
from utils import add_path

add_path()

from model.utils import common_params

MC = 200
T = common_params["T"]

def common_initial_settings():
    plt.rc('text', usetex=True)
    plt.rc('grid', color='magenta', alpha=1, linewidth=1.5)
    plt.rc('figure', facecolor='white')


def common_final_settings(axs: list[Axes]):
    axs[0].set_ylim(0.9, 1)
    axs[0].set_ylim(0,0.35)
    axs[0].set_ylim(0,0.35)

    