import json
import os
from random import randint
from typing import Literal

from .constants import CV, EV, PHEV, CarTypes

my_path = os.path.abspath(__file__).split(os.sep)
my_path[-1] = "data.json"

with open(os.sep.join(my_path), "r", encoding="utf-8") as plik:
    data = json.load(plik)
    car_params = data["cars"]


class Car:
    def __init__(
        self, release_year: int | None = None, release_month: int | None = None
    ) -> None:
        if release_year is None:
            release_year = -randint(0, self.lifetime)
        if release_month is None:
            release_month = randint(0, 11)
        self.release_year = release_year
        self.release_month = release_month

    def is_operational(self, year: int, month: int) -> bool:
        return (
            year - self.release_year + (month - self.release_month) / 12 < self.lifetime
        )

    @property
    def lifetime(self) -> int:
        return car_params[self.car_type]["lifetime"]

    @property
    def car_type(self) -> CarTypes:
        raise Exception("")

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        raise Exception("")


class Car_EV(Car):
    @property
    def car_type(self) -> CarTypes:
        return EV

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        return (
            kwargs["energy_factor"]
            * car_params[EV]["power_consumption"]
            * kwargs["energy_price"].get_price(year, month)
            / (100 * 1000)
        )


class Car_CV(Car):
    @property
    def car_type(self) -> CarTypes:
        return CV

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        return (
            car_params[CV]["fuel_consumption"]
            * kwargs["fuel_price"].get_price(year, month)
            / 100
        )


class Car_PHEV(Car):
    @property
    def car_type(self) -> CarTypes:
        return PHEV

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        return (
            kwargs["energy_factor"]
            * car_params[PHEV]["power_consumption"]
            * kwargs["energy_price"].get_price(year, month)
            / 1000
            + car_params[PHEV]["fuel_consumption"]
            * kwargs["fuel_price"].get_price(year, month)
        ) / 200
