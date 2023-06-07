from random import random
from typing import Any, Callable, Tuple, TypedDict, TypeVar

from ..Government import AbstractGovernment, GovernmentBuildChargingStation

# class CommonParamsKwargs(TypedDict):
#     # government: AbstractGovernment
#     government: Any
#     population: int
#     energy_price: int
#     fuel_price: int
#     nerby_radius: int
#     city_size: Tuple[int, int]
#     alpha: float
#     corporation_margin: float
#     corporation_technological_progress: float
#     initial_public_chargers: int
#     initial_time: Tuple[int, int]
#     car_price_noise: Any
#     # car_price_noise: Callable[[], float]
#     # car_price_noise: TypeVar('Callable[[], float]')

# # class CommonParams(TypedDict):
# #     T: int
# #     kwargs: CommonParamsKwargs
# cpk: CommonParamsKwargs = {
cpk = {
    "alpha": 0.01,
    "car_price_noise": lambda: random() * 10_000 - 5_000,
    "city_size": (54, 54),
    "corporation_margin": 0.2,
    "corporation_technological_progress": 0.004,
    "energy_price": 600,
    "energy_factor": 1,
    "fuel_price": 6,
    "government": GovernmentBuildChargingStation(new_chargers=10),
    "initial_public_chargers": 6,
    "initial_time": (2015, 1),
    "nerby_radius": 1,
    "population": 3_000,
}
common_params = {
    "T": 100,
    "kwargs": cpk,
}
