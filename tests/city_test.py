import random
from typing import Iterable, Tuple

import pytest

from model.City import City
from model.Customer import Customer


@pytest.mark.parametrize(
    "shape, initial_chargers",
    (
        ((100, 100), 10),
        ((10, 200), 15),
        ((310, 20), 30),
    ),
)
def test_city_initial(shape, initial_chargers):
    city = City(shape, initial_chargers)
    assert city.charger_pos is not None
    assert city.count_chargers() == initial_chargers
    assert ((city.charger_pos[:, 0] > 0) * (city.charger_pos[:, 0] < shape[0])).all()
    assert ((city.charger_pos[:, 1] > 0) * (city.charger_pos[:, 1] < shape[1])).all()


@pytest.mark.parametrize(
    "shape, initial, increase",
    (
        ((100, 100), 100, 10),
        ((10, 200), 200, 15),
        ((310, 20), 20, 30),
    ),
)
def test_build(shape, initial, increase):
    city = City(shape, initial)
    assert city.count_chargers() == initial
    for i in range(1, 10):
        city.build_new(increase)
        assert city.count_chargers() == initial + i * increase
    assert city.charger_pos is not None
    assert ((city.charger_pos[:, 0] > 0) * (city.charger_pos[:, 0] < shape[0])).all()
    assert ((city.charger_pos[:, 1] > 0) * (city.charger_pos[:, 1] < shape[1])).all()


@pytest.mark.parametrize(
    "initial, to_close",
    (
        (100, 10),
        (20, 13),
        (20, 20),
    ),
)
def test_close(initial, to_close):
    city = City((100, 100), initial)
    assert city.count_chargers() == initial
    for i in range(1, to_close + 1):
        city.close_charger(random.randint(0, city.count_chargers() - 1))
        assert city.count_chargers() == initial - i


@pytest.mark.parametrize(
    "initial, next_build",
    (
        (100, 10),
        (20, 13),
        (20, 20),
    ),
)
def test_close_build_close(initial, next_build):
    city = City((100, 100), initial)
    assert city.count_chargers() == initial
    for i in range(1, initial + 1):
        city.close_charger(random.randint(0, city.count_chargers() - 1))
        assert city.count_chargers() == initial - i
    assert city.count_chargers() == 0
    city.build_new(next_build)
    assert city.count_chargers() == next_build
    for i in range(1, next_build + 1):
        city.close_charger(random.randint(0, city.count_chargers() - 1))
        assert city.count_chargers() == next_build - i
    assert city.count_chargers() == 0


@pytest.mark.parametrize(
    "chargers_loc, customer_pos, radius, nearby_chargers",
    (
        (((0, 0) for _ in range(10)), (0, 0), 1, 10),
        ((*((0, 0) for _ in range(9)), (50, 50)), (0, 0), 1, 9),
        ((*((i, i) for i in range(9)), (50, 50)), (1, 1), 1, 1),
        ((*((i, i) for i in range(9)), (50, 50)), (1, 1), 1.5, 3),
    ),
)
def test_count_close_to(
    chargers_loc: Iterable[Tuple[int, int]],
    customer_pos: Tuple[float, float],
    radius: float,
    nearby_chargers: int,
):
    city_size = (100, 100)
    chargers_loc = tuple(chargers_loc)
    city = City(city_size, len(chargers_loc))
    assert city.charger_pos is not None
    for i, loc in enumerate(chargers_loc):
        city.charger_pos[i, 0] = loc[0]
        city.charger_pos[i, 1] = loc[1]
    customer = Customer(None, None, None, city_size)  # type: ignore
    customer._home = customer_pos
    assert city.count_nerby_chargers(customer, radius) == nearby_chargers
