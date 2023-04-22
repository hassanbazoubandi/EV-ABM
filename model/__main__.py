import matplotlib.pyplot as plt

from .Society import Society

N = 100
T = 100
soc = Society(N, 0.1, 0.2, 0.0004)
soc.go(T - 1)
# print(soc.get_historical_states())
plt.plot(soc.get_historical_states())
plt.show()
