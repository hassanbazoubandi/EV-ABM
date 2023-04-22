from typing import Tuple

from _typeshed import Incomplete

from .Cars import Car as Car
from .Cars import Car_CV as Car_CV
from .Cars import Car_EV as Car_EV
from .Cars import Car_PHEV as Car_PHEV
from .City import City as City
from .constants import CV as CV
from .constants import EV as EV
from .constants import PHEV as PHEV
from .constants import oc_h as oc_h
from .constants import oc_p as oc_p
from .constants import year_bev as year_bev
from .Corporations import Corporations as Corporations
from .Custormer import Customer as Customer
from .Goverment import Goverment as Goverment

class Society:
    alpha: Incomplete
    customers: Incomplete
    nerby_radius: Incomplete
    goverment: Incomplete
    corporations: Incomplete
    city: Incomplete
    state: Incomplete
    historical_states: Incomplete
    def __init__(
        self,
        population,
        alpha: float,
        corporation_margin: float,
        corporation_technological_progress: float,
        city_size: Tuple[int, int],
        nerby_radius: float,
        initial_public_chargers: int,
    ) -> None: ...
    def get_historical_states(self): ...
    def public_charging_nerby(self, customer): ...
    def go(self, N: int): ...
