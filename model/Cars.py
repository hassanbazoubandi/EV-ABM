"""
Cars, as a customer field, are responsible for type (BEV, PHEV, CV),
age and cost per km.
Any car type has own class witch inherit for class Car (like abstract class).
"""
from random import randint

from .common import get_data
from .constants import CV, EV, PHEV, CarTypes

data = get_data()
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

    def age(self, year: int, month: int):
        return year - self.release_year + (month - self.release_month) / 12
    
    @property
    def lifetime(self) -> int:
        return car_params[self.car_type]["lifetime"]

    @property
    def car_type(self) -> CarTypes:
        raise Exception("")

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        raise Exception("")


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
            * car_params[PHEV]["energy_consumption"]
            * kwargs["energy_price"].get_price(year, month)
            / 1000  # energy consumption in kWh, energy price in MWh
            + car_params[PHEV]["fuel_consumption"]
            * kwargs["fuel_price"].get_price(year, month)
        ) / 200


class Car_EV(Car):
    @property
    def car_type(self) -> CarTypes:
        return EV

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        return (
            kwargs["energy_factor"]
            * car_params[EV]["energy_consumption"]
            * kwargs["energy_price"].get_price(year, month)
            / (100 * 1000)  # energy consumption in kWh, energy price in MWh
        )
