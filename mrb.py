import os

import matplotlib.pyplot as plt

from model import (CV, EV, PHEV, GovernmentBuildChargingStation,
                   SocietyConstantsEnergyPrices)
from model.utils import (check_by, common_params, get_trajectories,  # New cell
                         plot_check_by, plot_intervals)

plt.style.use("dark_background")
plt.rc("grid", alpha=0.3)  # New cell
MC = 100
T = 90
N = common_params["kwargs"]["population"]


param = "alpha"
param_list = [0.01, 0.05, 0.1, 0.2, 0.4, 0.6]  # New cell
common_params["kwargs"]["initial_public_chargers"] = 100_000  # New cell
values = check_by(
    SocietyConstantsEnergyPrices, common_params["kwargs"], param, param_list, T, MC, 4
)  # New cell
fig, axs = plt.subplots(nrows=3, figsize=(10, 9))
plot_check_by(values, axs)

for ax in axs:
    ax.legend()
axs[0].set_title(CV)
axs[1].set_title(EV)
axs[2].set_title(PHEV)

# New cell
# fig, axs = plt.subplots(nrows=3, figsize=(10, 9))

# plot_intervals(
#     year / 12,
#     [trajectory / N for trajectory in CVs],
#     ax=axs[0],
#     color="c",
#     label="CV",
#     alpha=0.3,
# )
# plot_intervals(
#     year / 12,
#     [trajectory / N for trajectory in EVs],
#     ax=axs[1],
#     color="m",
#     label="EV",
#     alpha=0.3,
# )
# plot_intervals(
#     year / 12,
#     [trajectory / N for trajectory in PHEVs],
#     ax=axs[2],
#     color="y",
#     label="PHEV",
#     alpha=0.3,
# )


# axs[0].legend()
# axs[1].legend()
# axs[2].legend()

# axs[0].set_title("CV")
# axs[1].set_title("EV")
# axs[2].set_title("PHEV")

# fig.suptitle("constatnt prices, government build chargers stations", fontsize=16)# New cell
