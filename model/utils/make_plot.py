from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame


def plot_intervals(x, y: List[List[float]], ax=None, color=None, alpha=0.3, **kwargs):
    Y = np.array(y)
    if ax is None:
        ax = plt.subplot(1, 1, 1)
    Y_min = Y.min(0)
    Y_max = Y.max(0)
    ax.fill_between(x, Y_min, Y_max, Y_min <= Y_max, color=color, alpha=alpha)
    ax.plot(x, Y.mean(0), color=color, **kwargs)
    return ax


def plot_check_by(
    values: Dict[
        str, Tuple[List[DataFrame], List[DataFrame], List[DataFrame], DataFrame]
    ],
    axs: None | List[Any] = None,
):
    if axs is None:
        _, axs = plt.subplots(nrows=3)
    for key in values:
        N = sum([df[0] for df in values[key]])
        break
    N = N[0]
    for key in values:
        x = values[key][-1] / 12
        for i in range(3):
            axs[i].plot(x, np.array(values[key][i]).mean(0) / N, label=key)
    return axs
