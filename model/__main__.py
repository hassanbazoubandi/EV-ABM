print("__main__.py TODO soon :D")
# import os

# import matplotlib.pyplot as plt

# from .Government import GovernmentBuildChargingStation
# from .Society import Society

# N = 100
# T = 100
# get_full_path = lambda x: os.sep.join(["data", x])
# energy_prices = get_full_path("energy_price.csv")
# fuel_prices = get_full_path("fuel_price.csv")

# soc = Society(
#     population=N,
#     alpha=0.01,
#     government=GovernmentBuildChargingStation(),
#     corporation_margin=0.2,
#     corporation_technological_progress=0.0004,
#     city_size=(500, 500),
#     nerby_radius=10,
#     initial_public_chargers=100,
#     initial_time=(2005, 5),
#     energy_prices_csv=energy_prices,
#     fuel_prices_csv=fuel_prices,
# )

# soc.run(T - 1)
# data = soc.get_historical_states()
# plt.plot(data["year"], data["CV"], label="CV")
# plt.plot(data["year"], data["EV"], label="EV")
# plt.plot(data["year"], data["PHEV"], label="PHEV")
# plt.legend()
# plt.savefig("./result.svg")
