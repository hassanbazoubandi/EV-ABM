import pytest

from model import CV, EV, PHEV
from model.Corporations import Corporations, in_money

car_types = [CV, EV, PHEV]

INITIAL_CARS_COST = {
    CV: 1_000.0,
    PHEV: 2_000.0,
    EV: 3_000.0,
}


@pytest.mark.parametrize(
    "value, cuted_value",
    (
        (10.0012, 10.0),
        (10.0125, 10.01),
        (10.129, 10.12),
        (23.446, 23.44),
    ),
)
def test_in_money(value, cuted_value):
    assert in_money(value) == cuted_value


def test_initial_cost():
    corporations = Corporations(0.1, 0.01)
    corporations.car_costs = INITIAL_CARS_COST.copy()
    for c_type in car_types:
        assert corporations.get_price(c_type) == in_money(
            INITIAL_CARS_COST[c_type] * 1.1
        )


def test_initial_cost_no_margin():
    corporations = Corporations(0.0, 0.01)
    corporations.car_costs = INITIAL_CARS_COST.copy()
    for c_type in car_types:
        assert corporations.get_price(c_type) == in_money(INITIAL_CARS_COST[c_type])


def test_technological_progress():
    corporations = Corporations(0.0, 0.5)
    corporations.car_costs = INITIAL_CARS_COST.copy()
    car_state = {
        CV: 10,
        PHEV: 20,
        EV: 90,
    }

    for i in range(1, 12):
        corporations.update(car_state, i)
        assert corporations.car_costs == INITIAL_CARS_COST

    for i in range(2):
        corporations.update(car_state, 0)
        assert corporations.get_price(CV) == INITIAL_CARS_COST[CV]
        assert corporations.get_price(EV) == in_money(
            INITIAL_CARS_COST[CV]
            + (INITIAL_CARS_COST[EV] - INITIAL_CARS_COST[CV]) * (0.1) ** (i + 1)
        )
        assert corporations.get_price(PHEV) == in_money(
            (corporations.get_price(CV) + corporations.get_price(EV)) / 2
        )
