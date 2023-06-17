#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt

from model import (CV, EV, PHEV, Car_EV, GovernmentBuildChargingStation,
                   GovernmentMixedStrategy, GovernmentProvidesSubsidies,
                   SocietyConstantsEnergyPrices)
from model.utils import check_by, common_params, plot_check_by

plt.style.use("dark_background")
plt.rc("grid", alpha=0.3)
MC = 8

N: int = common_params["kwargs"]["population"]
T: int = common_params["T"]
param = "government"

param_list = [
    GovernmentBuildChargingStation(),
    GovernmentMixedStrategy(PHEV_sub_scaler=0.1),
    GovernmentProvidesSubsidies(PHEV_sub_scaler=0.1),
]
name = "main_by_gov.png"


print(common_params["kwargs"])


values = check_by(
    SocietyConstantsEnergyPrices,
    common_params["kwargs"],
    param,
    param_list,
    T,
    MC,
    4,
)


fig, axs = plt.subplots(nrows=3)
plot_check_by(values, axs)

fig.set_facecolor("white")

for ax in axs:
    ax.set_xlabel("Year")
    ax.grid(alpha=0.1)

axs[0].set_title(CV)
axs[1].set_title(EV)
axs[2].set_title(PHEV)
fig.tight_layout()
fig.legend(
    [
        "Government build charging station",
        "Government mixed strategy",
        "Government provides subsidies",
    ],
    title=param.replace("_", " "),
    bbox_to_anchor=(17 / 16, -0.22),
    bbox_transform=axs[-1].transAxes,
    ncol=len(param),
)

plt.plot()

# EV jest typowe dla MC przy pierwszych krokach symulacji.
# Przez nowość prawdopodobnie EV jest ponad stan infrastruktury.
#


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

# fig.suptitle("constatnt prices, government build chargers stations", fontsize=16)
