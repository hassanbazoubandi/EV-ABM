from typing import Tuple

import pytest

from model.Cars import Car, Car_CV, Car_EV, Car_PHEV
from model.constants import CV, EV, PHEV, CarTypes
from model.Customer import Customer
from model.Government import (
    AbstractGovernment,
    GovernmentBuildChargingStation,
    GovernmentMixedStrategy,
    GovernmentProvidesSubsidies,
)


class Fake_Society:
    def __init__(self, gov: AbstractGovernment) -> None:
        self.government = gov


@pytest.mark.parametrize(
    "gov, car, profile, city_size",
    (
        (GovernmentMixedStrategy(), Car_EV(), PHEV, (10, 1000)),
        (GovernmentBuildChargingStation(), Car_CV(), EV, (10, 1000)),
        (GovernmentMixedStrategy(), Car_PHEV(), CV, (10, 1000)),
        (GovernmentProvidesSubsidies(), Car_EV(), PHEV, (10, 1000)),
    ),
)
def test_init_customer(
    gov: AbstractGovernment,
    car: Car,
    profile: CarTypes,
    city_size: Tuple[float, float],
):
    soc = Fake_Society(gov)
    customer = Customer(soc, car, profile, city_size)
    home = customer.home
    assert home[0] >= 0
    assert home[0] <= city_size[0]
    assert home[1] >= 0
    assert home[1] <= city_size[1]


@pytest.mark.parametrize(
    "car, profile, today, is_working",
    (
        (Car_EV(0, 0), PHEV, (1, 10), True),
        (Car_CV(0, 0), EV, (1, 10), True),
        (Car_PHEV(0, 0), CV, (1, 10), True),
        (Car_EV(0, 0), PHEV, (100, 10), False),
        (Car_CV(0, 0), EV, (100, 10), False),
        (Car_PHEV(0, 0), CV, (100, 10), False),
    ),
)
def test_customer_have_working_car(
    car: Car,
    profile: CarTypes,
    today: Tuple[int, int],
    is_working: bool,
):
    city_size = (100, 100)
    soc = Fake_Society(GovernmentMixedStrategy())
    customer = Customer(soc, car, profile, city_size)
    assert customer.have_working_car(*today) == is_working


@pytest.mark.parametrize(
    "car, profile, new_type",
    (
        (Car_EV(0, 0), PHEV, CV),
        (Car_CV(0, 0), EV, CV),
        (Car_PHEV(0, 0), CV, EV),
        (Car_EV(0, 0), PHEV, PHEV),
        (Car_CV(0, 0), EV, EV),
        (Car_PHEV(0, 0), CV, PHEV),
    ),
)
def test_customer_new_car_buy(
    car: Car,
    profile: CarTypes,
    new_type: CarTypes,
):
    city_size = (100, 100)
    soc = Fake_Society(GovernmentMixedStrategy())
    customer = Customer(soc, car, profile, city_size)
    assert customer.get_car_type() == car.car_type
    customer.buy(new_type, 0, 0)
    assert customer.get_car_type() == new_type


@pytest.mark.parametrize(
    "car, profile, new_types, chosed",
    (
        (Car_EV(0, 0), PHEV, (CV, PHEV), PHEV),
        (Car_EV(0, 0), PHEV, (CV, EV), None),
        (Car_EV(0, 0), PHEV, (EV, PHEV), PHEV),
        (Car_EV(0, 0), EV, (CV, PHEV), PHEV),
        (Car_EV(0, 0), EV, (CV, EV), EV),
        (Car_EV(0, 0), EV, (EV, PHEV), EV),
        (Car_EV(0, 0), CV, (CV, PHEV), CV),
        (Car_EV(0, 0), CV, (CV, EV), CV),
        (Car_EV(0, 0), CV, (EV, PHEV), PHEV),
    ),
)
def test_customer_new_car_choose(
    car: Car,
    profile: CarTypes,
    new_types: Tuple[CarTypes, CarTypes],
    chosed: CarTypes | None,
):
    city_size = (100, 100)
    soc = Fake_Society(GovernmentMixedStrategy())
    customer = Customer(soc, car, profile, city_size)
    assert customer.get_car_type() == car.car_type
    customer.choose(*new_types, 0, 0)
    if chosed is None:
        assert (customer.get_car_type() == new_types[0]) or (
            customer.get_car_type() == new_types[1]
        )
    else:
        assert customer.get_car_type() == chosed
