import pytest
from typing import Tuple
from model.Cars import Car, Car_EV, Car_CV, Car_PHEV
from model.Customer import Customer
from model.Government import AbstractGovernment, GovernmentMixedStrategy
from model.constants import CarTypes, CV, EV, PHEV

class Fake_Society:
    def __init__(self, gov: AbstractGovernment) -> None:
        self.government = gov


@pytest.mark.parametrize(
    "gov,car,profile,city_size",
    (
        (GovernmentMixedStrategy(), Car_EV(), PHEV, (10, 1000))
    ),
)
def test_init_customer(
    gov: AbstractGovernment,
    car: Car,
    profile: CarTypes,
    city_size: Tuple[float, float],
):
    pass
    # soc = Fake_Society(gov)
    # customer = Customer(soc, car, profile, city_size)
    # home = customer.home
    # assert home[0] >= 0
    # assert home[0] <= city_size[0]
    # assert home[1] >= 0
    # assert home[1] <= city_size[1]

