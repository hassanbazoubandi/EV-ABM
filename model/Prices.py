"""
Price is responsible for fuel and energy prices. 
In the default society "SocietyConstantsEnergyPrices" (see Society)
is used class ConstatntPrice and are constants prices.
Howeover model is ready for implement function wich estimate future prices (class Prices).
Both of them (ConstatntPrice, Prices) inherit for class Price.
"""
from math import isnan
from typing import Callable, Tuple

import pandas as pd

from .constants import price_col_names


class Price:
    def __init__(self, *args) -> None:
        pass

    def get_price(self, year: int, month: int) -> float:
        raise Exception("")


class Prices(Price):
    """
    Class implemented class Price for model.
    Class can be used for non-constant-price scenarios.
    """

    def __init__(
        self,
        data_file: str | pd.DataFrame,
        predict_model: Callable[[pd.DataFrame, int, int], pd.DataFrame] | None = None,
        predict_to: Tuple[int, int] | None = None,
    ) -> None:
        """Class for non constants prices.
        Class can be used for both historical data and a model predictive of future data.

        Args:
            data_file (str | pd.DataFrame): name of file with data or df, with columns: ["year", "month", "price"]
            predict_model (Callable[[pd.DataFrame, int, int], pd.DataFrame] | None, optional): Function witch predict future price.
                Function have to get tree args: pd.DataFrame with real data to estimate future prices, year, month.
                Year and month is the time horizon for predicting data. If None, the data is not predicted.  Defaults to None.
            predict_to (Tuple[int, int] | None, optional): time horizont to predict data. Defaults to None.

        Raises:
            AttributeError: data_file must have str or pd.DataFrame.
            AttributeError: f"Prices data have to have ["year", "month", "price"] columns.
        """
        if isinstance(data_file, str):
            self.df_price = pd.read_csv(data_file)
        elif isinstance(data_file, pd.DataFrame):
            self.df_price = data_file
        else:
            raise AttributeError(
                f"data_file must have str or pd.DataFrame type not {type(data_file)}"
            )

        if predict_model is not None:
            self.df_price = predict_model(
                self.df_price, predict_to[0], predict_to[1]
            )  # noqa
        for col_name in price_col_names:
            if col_name not in self.df_price.columns:
                raise AttributeError(
                    f"Prices data have to have {price_col_names} columns."
                )

    def get_price(self, year: int, month: int) -> float:
        """Get price for seted date.

        Args:
            year (int): The year from which the price is to be gotten.
            month (int): The month from which the price is to be gotten.

        Raises:
            KeyError: Error is raised if there is no price for a given date.

        Returns:
            float: _description_
        """
        ret = self.df_price[
            (self.df_price["year"] == year) & (self.df_price["month"] == month)
        ]["price"].mean()
        if isnan(ret):
            raise KeyError(f"{year}.{month} price is not defined")
        return ret


class ConstatntPrice(Price):
    """
    Class implemented class Price for model.
    Class can be used for constant-price scenarios.
    """

    def __init__(self, price: float) -> None:
        """Class for model with constant price.

        Args:
            price (float): Price value
        """
        self.price = price

    def get_price(self, *args) -> float:
        """Get price.

        Returns:
            float: price
        """
        return self.price
