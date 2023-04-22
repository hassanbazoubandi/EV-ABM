from _typeshed import Incomplete

from .constants import CV as CV
from .constants import EV as EV
from .constants import PHEV as PHEV

class Corporations:
    margin: Incomplete
    technological_progress: Incomplete
    car_costs: Incomplete
    def __init__(self, margin, technological_progress) -> None: ...
    @property
    def CV_price(self): ...
    @property
    def PHEV_price(self): ...
    @property
    def EV_price(self): ...
    def update(self, current_state) -> None: ...
