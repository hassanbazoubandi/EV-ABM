import json
from random import randint
from typing import Literal

from .constants import CV, EV, PHEV, CarTypes

with open("model/data.json", "r") as plik:
    data = json.load(plik)
    car_params = data["cars"]

fuel_cost = 0
energy_cost = 0
print("TODO energy & fuel cost")


class Car:
    def __init__(
        self, release_year: int | None = None, release_month: int | None = None
    ) -> None:
        if release_year is None:
            release_year = -randint(0, self.lifetime - 1)
        if release_month is None:
            release_month = randint(1, 12)
        self.release_year = release_year
        self.release_month = release_month

    def is_operational(self, year: int, month: int) -> bool:
        return (
            year - self.release_year + (month - self.release_month) / 12 < self.lifetime
        )

    @property
    def lifetime(self):
        return car_params[self.car_type]["lifetime"]

    @property
    def car_type(self) -> CarTypes:
        raise Exception("")

    @staticmethod
    def cost_per_km(year, month, **kwargs):
        raise Exception("")


class Car_EV(Car):
    @property
    def car_type(self) -> CarTypes:
        return EV

    @staticmethod
    def cost_per_km(year, month, **kwargs):
        return (
            kwargs["energy_factor"]
            * car_params[EV]["power_consumption"]
            * energy_cost
            / 100
        )


class Car_CV(Car):
    @property
    def car_type(self) -> CarTypes:
        return CV

    @staticmethod
    def cost_per_km(year, month, **kwargs):
        return car_params[CV]["fuel_consumption"] * fuel_cost / 100


class Car_PHEV(Car):
    @property
    def car_type(self) -> CarTypes:
        return PHEV

    @staticmethod
    def cost_per_km(year, month, **kwargs):
        return (
            kwargs["energy_factor"]
            * car_params[PHEV]["power_consumption"]
            * energy_cost
            + car_params[PHEV]["fuel_consumption"] * fuel_cost
        ) / 200
