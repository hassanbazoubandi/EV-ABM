from .Cars import Car as Car, Car_CV as Car_CV, Car_EV as Car_EV, Car_PHEV as Car_PHEV
from .City import City as City
from .Corporations import Corporations as Corporations
from .Customer import Customer as Customer
from .Goverment import Goverment as Goverment
from .constants import CV as CV, EV as EV, PHEV as PHEV, oc_h as oc_h, oc_p as oc_p, year_bev as year_bev
from _typeshed import Incomplete
from typing import Tuple

class Society:
    alpha: Incomplete
    customers: Incomplete
    nerby_radius: Incomplete
    goverment: Incomplete
    corporations: Incomplete
    city: Incomplete
    state: Incomplete
    historical_states: Incomplete
    def __init__(self, population, alpha: float, corporation_margin: float, corporation_technological_progress: float, city_size: Tuple[int, int], nerby_radius: float, initial_public_chargers: int) -> None: ...
    def get_historical_states(self): ...
    def public_charging_nerby(self, customer: Customer) -> bool: ...
    def go(self, N: int): ...
