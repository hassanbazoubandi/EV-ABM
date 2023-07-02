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
    """Customer represent type of one model agent.
    Customers are agents whose status will be counted and analyzed.
    Any Customer instance has indyvidual set of fields.
    - procfile -- mean annual mileage
    - home -- place in City
    - car -- see class Car

    The customer is also responsible for the mechanism for buying a car
    and for choosing between two types.
    """

    def __init__(
        self,
        society: "Society",  # noqa
        car: Car,
        profile: CarTypes,
        city_size: Tuple[float, float],
    ) -> None:
        """Customer represent type of one model agent.
            Customers are agents whose status will be counted and analyzed.

        Args:
            society (Society): society
            profile (CarTypes): Customer profile (average annual mileage)
            city_size (Tuple[float, float]): City size to random draw home place.
        """
        self.society = society
        self.car = car
        self.profile = profile
        self._home = (
            random() * city_size[0],
            random() * city_size[1],
        )

    def have_working_car(self, year: int, month: int) -> bool:
        """This method compare actual car are and them lifetime.
        Car is working if his age < lifetime.

        Args:
            year (int): Current year.
            month (int): Current month.

        Returns:
            bool: True if customers car is working, False in other case.
        """
        return self.car.is_operational(year, month)

    def get_car_type(self) -> CarTypes:
        """Get customers car type.

        Returns:
            CarTypes: Customers car type.
        """
        return self.car.car_type

    def buy(self, car_type: CarTypes, current_year: int, current_month: int):
        """Buy new car with seted type

        Args:
            car_type (CarTypes): Type of car to buy.
            year (int): Current year.
            month (int): Current month.
        """
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
        """Chose betwean two car types and buy one.

        Args:
            car_type1 (CarTypes): First car type to buy.
            car_type2 (CarTypes): Second car type to buy.
            current_year (int): Current year.
            current_month (int): Current month.
        """
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
        """Get position of customer's house.

        Returns:
            Tuple[float, float]: Position of customer's house.
        """
        return self._home
