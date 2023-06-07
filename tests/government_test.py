import pytest
from model.Government import (
    GovernmentBuildChargingStation,
    GovernmentMixedStrategy,
    GovernmentProvidesSubsidies,
)
from model.constants import CV, EV, PHEV
from model.City import City

CITY_SIZE = (100,100)

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
        gov.update(i%12)


@pytest.mark.parametrize(
    "initial_chargers, new_chargers",
    (
        (10, 100),
        (100, 10),
    ),
)
def test_GBCS_build(initial_chargers, new_chargers):
    gov = GovernmentBuildChargingStation(new_chargers=new_chargers)
    soc = Fake_Society(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert soc.city.count_chargers() == initial_chargers + ((i-1)//12 + 1)* new_chargers
        gov.update(i%12)

@pytest.mark.parametrize(
    "one_subsidity_level, year_subsidies",
    (
        (30_000, 10_000),
    ),
)
def test_GPS_subsid(one_subsidity_level, year_subsidies):
    gov = GovernmentProvidesSubsidies(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=year_subsidies
    )

    gov.set_society(Fake_Society(City(CITY_SIZE, 0)))
    
    for i in range(20):
        if i%12 == 0:
            assert gov.get_subsidy(EV) == one_subsidity_level
            assert gov.get_subsidy(PHEV) == one_subsidity_level
            assert gov.get_subsidy(CV) == 0
        else:
            assert gov.get_subsidy(EV) == 0
            assert gov.get_subsidy(PHEV) == 0
            assert gov.get_subsidy(CV) == 0

        gov.update(i%12)


@pytest.mark.parametrize(
    "initial_chargers",
    (
        (10),
        (100),
    ),
)
def test_GPS_build(initial_chargers):
    gov = GovernmentProvidesSubsidies(one_subsidity_level=10_000, year_subsidies=40_000)
    soc = Fake_Society(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert soc.city.count_chargers() == initial_chargers
        gov.update(i%12)


def test_GPS_subsid(one_subsidity_level, year_subsidies):
    gov = GovernmentProvidesSubsidies(
        one_subsidity_level=one_subsidity_level,
        year_subsidies=year_subsidies
    )

    gov.set_society(Fake_Society(City(CITY_SIZE, 0)))
    
    for i in range(20):
        if i%12 == 0:
            assert gov.get_subsidy(EV) == one_subsidity_level
            assert gov.get_subsidy(PHEV) == one_subsidity_level
            assert gov.get_subsidy(CV) == 0
        else:
            assert gov.get_subsidy(EV) == 0
            assert gov.get_subsidy(PHEV) == 0
            assert gov.get_subsidy(CV) == 0

        gov.update(i%12)



@pytest.mark.parametrize(
    "initial_chargers, new_chargers",
    (
        (10, 100),
        (100, 10),
    ),
)
def test_GBCS_build(initial_chargers, new_chargers):
    gov = GovernmentBuildChargingStation(new_chargers=new_chargers)
    soc = Fake_Society(City(CITY_SIZE, initial_chargers))
    gov.set_society(soc)

    for i in range(20):
        assert soc.city.count_chargers() == initial_chargers + ((i-1)//12 + 1)* new_chargers
        gov.update(i%12)

