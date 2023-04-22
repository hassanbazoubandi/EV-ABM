from typing import Tuple

from _typeshed import Incomplete

from .Cars import Car as Car

class Customer:
    car: Incomplete
    profile: Incomplete
    def __init__(
        self, car: Car, profile: int, city_size: Tuple[float, float]
    ) -> None: ...
    def have_working_car(self, year: int): ...
    def get_car_type(self): ...
    @property
    def home(self): ...
