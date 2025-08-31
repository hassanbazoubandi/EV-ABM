#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt

from model import (
    CV,
    EV,
    PHEV,
    GovernmentBuildChargingStation,
    GovernmentMixedStrategy,
    GovernmentNoSubsidies,
    GovernmentProvidesSubsidies,
    SocietyConstantsEnergyPrices,
)
from model.utils import check_by, common_params, plot_check_by

plt.rc("text", usetex=True)
plt.rc("grid", color="magenta", alpha=1, linewidth=1.5)
plt.rc("figure", facecolor="white")

MC = 200


T: int = common_params["T"]
param = "government"

param_list = [
    GovernmentBuildChargingStation(),
    GovernmentMixedStrategy(),
    GovernmentProvidesSubsidies(),
    GovernmentNoSubsidies(),
]
name = "example_main_by_gov.png"

title = "Results by different Government strategies."
print("{")
for key in common_params["kwargs"]:
    print(f"    {key}: {common_params['kwargs'][key]}")
print("}")


values = check_by(
    SocietyConstantsEnergyPrices,
    common_params["kwargs"],
    param,
    param_list,
    T,
    MC,
    4,
)

fig, axs = plt.subplots(nrows=3, figsize=(8, 8))
plot_check_by(values, axs)

fig.suptitle(title, fontsize=16, y=1)

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
        "Baseline Government ",
    ],
    title=param.replace("_", " "),
    bbox_to_anchor=(17 / 16, -0.22),
    bbox_transform=axs[-1].transAxes,
    ncol=len(param),
)

plt.savefig(name, bbox_inches="tight")
