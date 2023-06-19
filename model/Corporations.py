from typing import Dict

from .common import get_data
from .constants import CV, EV, PHEV, CarTypes

data = get_data()
car_params = data["cars"]


def in_money(value: float) -> float:
    return int(value * 100) / 100


class Corporations:
    def __init__(self, margin: float, technological_progress: float) -> None:
        self.margin = margin
        self.technological_progress = technological_progress
        self.car_costs: Dict[CarTypes, float] = {
            CV: car_params[CV]["cost"] / (1 + self.margin),
            EV: car_params[EV]["cost"] / (1 + self.margin),
            PHEV: car_params[PHEV]["cost"] / (1 + self.margin),
        }

    def get_price(self, c_type: CarTypes) -> float:
        return in_money((1 + self.margin) * self.car_costs[c_type])

    def update(self, current_state: Dict[CarTypes, int], current_month: int) -> None:
        if current_month:
            return
        if (current_state[EV] + current_state[PHEV]) == 0:
            return
        ev_under = self.car_costs[EV] - self.car_costs[CV]
        ev_under *= (current_state[EV] + current_state[PHEV] / 2) ** (
            -self.technological_progress
        )
        self.car_costs[EV] = self.car_costs[CV] + ev_under
        self.car_costs[PHEV] = (self.car_costs[EV] + self.car_costs[CV]) / 2
        for key in self.car_costs:
            self.car_costs[key] = in_money(self.car_costs[key])

