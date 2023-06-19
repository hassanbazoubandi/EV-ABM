import random

import pytest

from model.City import City
from model.constants import CV, EV, PHEV, CarTypes
from model.Government import (
    GovernmentBuildChargingStation,
    GovernmentMixedStrategy,
    GovernmentProvidesSubsidies,
    _get_subsidity_val,
)

CITY_SIZE = (100, 100)


class FakeSociety:
    def __init__(self, city: City) -> None:
        self.city = city


def test_GBCS_subsid():
    gov = GovernmentBuildChargingStation()
    gov.set_society(FakeSociety(City(CITY_SIZE, 0)))
    for i in range(20):
        for _ in range(10):
            assert gov.get_subsidy(EV) == 0
            assert gov.get_subsidy(PHEV) == 0
            assert gov.get_subsidy(CV) == 0
        gov.update(i % 12)


@pytest.mark.parametrize(
    "initial_chargers, new_chargers",
    (
        (10, 100),
        (100, 10),
    ),
)
def test_GBCS_build(initial_chargers: int, new_chargers: int):
    gov = GovernmentBuildChargingStation(new_chargers=new_chargers)
    soc = FakeSociety(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert (
            soc.city.count_chargers()
            == initial_chargers + ((i - 1) // 12 + 1) * new_chargers
        )
        gov.update(i % 12)


@pytest.mark.parametrize(
    "one_subsidity_level, n_annual_subsidies",
    (
        (10_000, 3),
        (100, 30),
    ),
)
def test_GPS_subsid(one_subsidity_level: int, n_annual_subsidies: int):
    gov = GovernmentProvidesSubsidies(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=n_annual_subsidies * one_subsidity_level,
        PHEV_sub_scaler=1,
    )

    gov.set_society(FakeSociety(City(CITY_SIZE, 0)))

    for i in range(1, 26):
        if i % 12 == 1:
            for _ in range(n_annual_subsidies):
                if random.random() < 1 / 2:
                    assert gov.get_subsidy(EV) == one_subsidity_level
                else:
                    assert gov.get_subsidy(PHEV) == one_subsidity_level
            assert gov.get_subsidy(CV) == 0
            assert gov.get_subsidy(EV) == 0
            assert gov.get_subsidy(PHEV) == 0
        else:
            assert gov.get_subsidy(EV) == 0
            assert gov.get_subsidy(PHEV) == 0
            assert gov.get_subsidy(CV) == 0

        gov.update(i % 12)


@pytest.mark.parametrize(
    "initial_chargers",
    (
        (10),
        (100),
    ),
)
def test_GPS_build(initial_chargers: int):
    gov = GovernmentProvidesSubsidies(
        one_subsidity_level=10_000,
        year_subsidies=40_000,
        PHEV_sub_scaler=1,
    )
    soc = FakeSociety(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert soc.city.count_chargers() == initial_chargers
        gov.update(i % 12)


@pytest.mark.parametrize(
    "one_subsidity_level, n_annual_subsidies",
    (
        (10_000, 3),
        (10, 12),    
    ),
)
def test_GM_subsid(one_subsidity_level: int, n_annual_subsidies: int):
    gov = GovernmentMixedStrategy(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=n_annual_subsidies * one_subsidity_level,
        PHEV_sub_scaler=1,
    )

    gov.set_society(FakeSociety(City(CITY_SIZE, 0)))
    for i in range(1, 26):
        if i % 12 == 1:
            for _ in range(n_annual_subsidies):
                if random.random() < 1 / 2:
                    assert gov.get_subsidy(EV) == one_subsidity_level
                else:
                    assert gov.get_subsidy(PHEV) == one_subsidity_level
            assert gov.get_subsidy(CV) == 0
            assert gov.get_subsidy(EV) == 0
            assert gov.get_subsidy(PHEV) == 0
        else:
            assert gov.get_subsidy(EV) == 0
            assert gov.get_subsidy(PHEV) == 0
            assert gov.get_subsidy(CV) == 0

        gov.update(i % 12)


@pytest.mark.parametrize(
    "one_subsidity_level, n_annual_subsidies",
    (
        (10_000, 3),
        (100, 9),
    ),
)
def test_GM_subsid_dont_stack(one_subsidity_level: int, n_annual_subsidies: int):
    gov = GovernmentMixedStrategy(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=n_annual_subsidies * one_subsidity_level,
        PHEV_sub_scaler=1,
    )

    gov.set_society(FakeSociety(City(CITY_SIZE, 0)))
    for i in range(1, 26):
        gov.update(i % 12)
    for _ in range(n_annual_subsidies):
        if random.random() < 1 / 2:
            assert gov.get_subsidy(EV) == one_subsidity_level
        else:
            assert gov.get_subsidy(PHEV) == one_subsidity_level
    assert gov.get_subsidy(CV) == 0
    assert gov.get_subsidy(EV) == 0
    assert gov.get_subsidy(PHEV) == 0


@pytest.mark.parametrize(
    "initial_chargers, new_chargers",
    (
        (10, 100),
        (100, 10),
    ),
)
def test_GM_build(initial_chargers: int, new_chargers: int):
    gov = GovernmentMixedStrategy(new_chargers=new_chargers)
    soc = FakeSociety(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert (
            soc.city.count_chargers()
            == initial_chargers + ((i - 1) // 12 + 1) * new_chargers
        )
        gov.update(i % 12)


@pytest.mark.parametrize(
    "budget, sub_val, car_type, EV_scalar, PHEV_scalar, CV_scalar, val",
    (
        *[(1e5, 100, c_type, 1,1,1, 100) for c_type in [CV, PHEV, EV]],
        (1e5, 100, CV, 1/2,1,1, 100),
        (1e5, 100, CV, 1,1/2,1, 100),
        (1e5, 100, CV, 1,1,1/2, 50),
        (1e5, 100, PHEV, 1/2,1,1, 100),
        (1e5, 100, PHEV, 1,1/2,1, 50),
        (1e5, 100, PHEV, 1,1,1/2, 100),
        (1e5, 100, EV, 1/2,1,1, 50),
        (1e5, 100, EV, 1,1/2,1, 100),
        (1e5, 100, EV, 1,1,1/2, 100),
    ),
)
def test_get_subsidity_val(
    budget: int,
    sub_val: int,
    car_type: CarTypes,
    EV_scalar: float,
    PHEV_scalar: float,
    CV_scalar: float,
    val: float,
):
    assert val == _get_subsidity_val(budget, sub_val, car_type, EV_scalar, PHEV_scalar, CV_scalar)

