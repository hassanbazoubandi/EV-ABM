from typing import Type

import pytest

from model.Cars import Car, Car_CV, Car_EV, Car_PHEV
from model.constants import CV, EV, PHEV, CarTypes


@pytest.mark.parametrize(
    "c_type, CarClass",
    (
        (CV, Car_CV),
        (EV, Car_EV),
        (PHEV, Car_PHEV),
    ),
)
def test_car_type(c_type: CarTypes, CarClass: Type[Car]):
    car = CarClass(1, 1)
    life_time = car.lifetime
    assert car.car_type == c_type
    assert car.is_operational(1 + life_time, 0)
    assert not car.is_operational(1 + life_time, 1)
    assert not car.is_operational(1 + life_time, 2)
