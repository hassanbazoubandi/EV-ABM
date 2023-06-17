import os
from typing import Tuple

import pandas as pd
from hypothesis import given
from hypothesis import strategies as st

from model.Prices import ConstatntPrice, Prices

data_file = os.sep.join(["data", "energy_price.csv"])
energy_price = pd.read_csv(data_file)
min_year = energy_price["year"].min() + 1
max_year = energy_price["year"].max() - 1
time_horizont = 2100

FAKE_CONSTANT_VALUE = 10.22


def constatnt_model(df: pd.DataFrame, year: int, month: int):
    last_year = df["year"].max()
    last_month = df[df["year"] == last_year]["month"].max()
    new_rows = []
    while last_year < year or last_month < month:
        last_month += 1
        if last_month == 13:
            last_year += 1
            last_month = 1
        new_rows.append(
            {
                "year": last_year,
                "month": last_month,
                "day": 1,
                "price": FAKE_CONSTANT_VALUE,
            }
        )
    return pd.concat([df, pd.DataFrame(new_rows)])


@given(year=st.integers(), month=st.integers(min_value=1, max_value=12))
def test_ConstatntPrice(year, month):
    price = ConstatntPrice(11.2)
    assert 11.2 == price.get_price(year, month)


@given(
    year=st.integers(min_value=min_year, max_value=max_year),
    month=st.integers(min_value=1, max_value=12),
)
def test_Prices_no_model(year, month):
    price = Prices(energy_price)
    assert energy_price[
        (energy_price["year"] == year) & (energy_price["month"] == month)
    ]["price"].mean() == price.get_price(year, month)


@given(
    year=st.integers(min_value=max_year + 2, max_value=time_horizont - 1),
    month=st.integers(min_value=1, max_value=12),
)
def test_Prices_constant_model(year, month):
    price = Prices(energy_price.copy(), constatnt_model, (time_horizont, 1))
