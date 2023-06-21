"""
Customer represent type of one model agent. 
Customers are agents whose status will be counted and analyzed.
Any Customer instance has indyvidual set of fields.
- procfile -- mean annual mileage
- home -- place in City
- car -- see class Car

The customer is also responsible for the mechanism for buying a car
and for choosing between two types.
"""
from random import random
from typing import Tuple

from .Cars import Car, Car_CV, Car_EV, Car_PHEV
from .constants import CV, EV, PHEV, CarTypes


class Customer:
    def __init__(
        self,
        society: "Society",  # noqa
        car: Car,
        profile: CarTypes,
        city_size: Tuple[float, float],
    ) -> None:
        self.society = society
        self.car = car
        self.profile = profile
        self._home = (
            random() * city_size[0],
            random() * city_size[1],
        )

    def have_working_car(self, year: int, month: int) -> bool:
        return self.car.is_operational(year, month)

    def get_car_type(self) -> CarTypes:
        return self.car.car_type

    def buy(self, car_type: CarTypes, current_year: int, current_month: int):
        self.society.government.get_subsidy(car_type)
        if car_type == EV:
            self.car = Car_EV(current_year, current_month)
        elif car_type == CV:
            self.car = Car_CV(current_year, current_month)
        elif car_type == PHEV:
            self.car = Car_PHEV(current_year, current_month)

    def choose(
        self,
        car_type1: CarTypes,
        car_type2: CarTypes,
        current_year: int,
        current_month: int,
    ):
        if self.profile in (car_type1, car_type2):
            self.buy(self.profile, current_year, current_month)
        elif self.profile in (CV, EV):
            self.buy(PHEV, current_year, current_month)
        elif random() < 1 / 2:
            self.buy(car_type1, current_year, current_month)
        else:
            self.buy(car_type2, current_year, current_month)

    @property
    def home(self) -> Tuple[float, float]:
        return self._home
