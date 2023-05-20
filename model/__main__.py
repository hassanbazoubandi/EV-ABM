import matplotlib.pyplot as plt

from .Society import Society

N = 100
T = 100
soc = Society(N, 0.01, 0.2, 0.0004, (100, 100), 10, 10, (2023, 5))
soc.go(T - 1)
data = soc.get_historical_states()
plt.plot(data["year"], data["CV"], label="CV")
plt.plot(data["year"], data["EV"], label="EV")
plt.plot(data["year"], data["PHEV"], label="PHEV")
plt.legend()
plt.savefig("./result.svg")
