from random import random
from typing import Tuple

from .Cars import Car, Car_CV, Car_EV, Car_PHEV
from .constants import CV, EV, PHEV, CarTypes


class Customer:
    def __init__(self, car: Car, profile: int, city_size: Tuple[float, float]) -> None:
        self.car = car
        self.profile = profile
        self._home = (
            random() * city_size[0],
            random() * city_size[1],
        )

    def have_working_car(self, year: int) -> bool:
        return self.car.is_operational(year)

    def get_car_type(self) -> CarTypes:
        return self.car.car_type

    def buy(self, car_type: CarTypes, current_year: int):
        if car_type == EV:
            self.car = Car_EV(current_year)
        elif car_type == CV:
            self.car = Car_CV(current_year)
        elif car_type == PHEV:
            self.car = Car_PHEV(current_year)

    def choose(self, car_type1, car_type2, current_year):
        print("Customer.choose TODO")
        if random() < 1 / 2:
            self.buy(car_type1, current_year)
        else:
            self.buy(car_type2, current_year)

    @property
    def home(self):
        return self._home
