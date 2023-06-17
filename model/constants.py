from typing import Literal

CarTypes = Literal["CV", "BEV", "PHEV"]

CV: CarTypes = "CV"
EV: CarTypes = "BEV"
PHEV: CarTypes = "PHEV"

price_col_names = ["year", "month", "price"]
