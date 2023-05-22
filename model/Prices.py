from typing import Callable, Tuple
import pandas as pd

from .constants import price_col_names

class Prices:
    def __init__(
        self,
        data_file: str | pd.DataFrame,
        predict_model: Callable[[pd.DataFrame, Tuple[int, int]], pd.DataFrame] | None = None,
        predict_to: Tuple[int, int] | None = None,
    ) -> None:
        if isinstance(data_file, str):
            self.df = pd.read_csv(data_file)
        elif isinstance(data_file, pd.DataFrame):
            self.df = data_file
        else:
            raise AttributeError(
                f"data_file must have str or pd.DataFrame type not {type(data_file)}"
            )

        if predict_model is not None:
            self.df = predict_model(self.df, *predict_to)
        for col_name in price_col_names:
            if col_name not in self.df.columns:
                raise AttributeError(f"Prices data have to have {price_col_names} columns.")
        

    def get_price(self, year: int, month: int):
        return self.df[(self.df["year"] == year) & (self.df["month"] == month)]['price'].mean()

