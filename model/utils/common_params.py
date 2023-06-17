from random import random

from ..Government import GovernmentBuildChargingStation

cpk = {
    "alpha": 0.01,
    "car_price_noise": lambda: random() * 10_000 - 5_000,
    "city_size": (17, 17),
    "corporation_margin": 0.2,
    "corporation_technological_progress": 0.004,
    "energy_price": 500,
    "energy_factor": 0.8,
    "fuel_price": 6,
    "government": GovernmentBuildChargingStation(),
    "initial_public_chargers": 1,
    "initial_time": (2015, 1),
    "nerby_radius": 1,
    "population": 3_000,
}

common_params = {
    "T": 12 * 25,
    "kwargs": cpk,
}
