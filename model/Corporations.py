import json
from typing import Dict
from .constants import CV, EV, PHEV, CarTypes

with open("model/data.json", "r") as plik:
    data = json.load(plik)
    car_params = data["cars"]


def in_PLN(value: float) -> float:
    return int(value*100) / 100

class Corporations:
    def __init__(self, margin: float, technological_progress: float) -> None:
        self.margin = margin
        self.technological_progress = technological_progress
        self.car_costs: Dict[CarTypes, float] = {
            CV: car_params[CV]["cost"],
            EV: car_params[EV]["cost"],
            PHEV: car_params[PHEV]["cost"],
        }

    def get_price(self, c_type: CarTypes) -> int:
        return int((1 + self.margin) * self.car_costs[c_type])

    def update(self, current_state: Dict[CarTypes, int]) -> None:
        if (current_state[EV] + current_state[PHEV]) != 0:
            self.car_costs[EV] *= (current_state[EV] + current_state[PHEV] / 2) ** (-self.technological_progress)
        self.car_costs[PHEV] = (current_state[EV] + current_state[CV]) / 2
        for key in self.car_costs:
            self.car_costs[key] = in_PLN(self.car_costs[key])
            
