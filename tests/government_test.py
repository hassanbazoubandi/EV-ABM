import random

import pytest

from model.City import City
from model.constants import CV, EV, PHEV
from model.Government import (GovernmentBuildChargingStation,
                              GovernmentMixedStrategy,
                              GovernmentProvidesSubsidies)

CITY_SIZE = (100, 100)


class Fake_Society:
    def __init__(self, city: City) -> None:
        self.city = city


def test_GBCS_subsid():
    gov = GovernmentBuildChargingStation()
    gov.set_society(Fake_Society(City(CITY_SIZE, 0)))
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
    soc = Fake_Society(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert (
            soc.city.count_chargers()
            == initial_chargers + ((i - 1) // 12 + 1) * new_chargers
        )
        gov.update(i % 12)


@pytest.mark.parametrize(
    "one_subsidity_level, n_annual_subsidies",
    ((10_000, 3),),
)
def test_GPS_subsid(one_subsidity_level: int, n_annual_subsidies: int):
    gov = GovernmentProvidesSubsidies(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=n_annual_subsidies * one_subsidity_level,
    )

    gov.set_society(Fake_Society(City(CITY_SIZE, 0)))

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
    gov = GovernmentProvidesSubsidies(one_subsidity_level=10_000, year_subsidies=40_000)
    soc = Fake_Society(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert soc.city.count_chargers() == initial_chargers
        gov.update(i % 12)


@pytest.mark.parametrize(
    "one_subsidity_level, n_annual_subsidies",
    ((10_000, 3),),
)
def test_GM_subsid(one_subsidity_level: int, n_annual_subsidies: int):
    gov = GovernmentProvidesSubsidies(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=n_annual_subsidies * one_subsidity_level,
    )

    gov.set_society(Fake_Society(City(CITY_SIZE, 0)))
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
    ((10_000, 3),),
)
def test_GM_subsid_dont_stack(one_subsidity_level: int, n_annual_subsidies: int):
    gov = GovernmentProvidesSubsidies(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=n_annual_subsidies * one_subsidity_level,
    )

    gov.set_society(Fake_Society(City(CITY_SIZE, 0)))
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
    gov = GovernmentBuildChargingStation(new_chargers=new_chargers)
    soc = Fake_Society(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert (
            soc.city.count_chargers()
            == initial_chargers + ((i - 1) // 12 + 1) * new_chargers
        )
        gov.update(i % 12)
