import json

from .constants import CV, EV, PHEV, CarTypes

with open("model/data.json", "r") as plik:
    data = json.load(plik)
    car_params = data["cars"]


class Corporations:
    def __init__(self, margin: float, technological_progress: float) -> None:
        self.margin = margin
        self.technological_progress = technological_progress
        self.car_costs = {
            CV: car_params[CV]["cost"],
            EV: car_params[EV]["cost"],
            PHEV: car_params[PHEV]["cost"],
        }

    def get_price(self, c_type: CarTypes) -> int:
        return int((1 + self.margin) * self.car_costs[c_type])

    def update(self, current_state):
        print("# Corporations.update do poprawy")
        if current_state[EV] != 0:
            self.car_costs[EV] *= current_state[EV] ** (-self.technological_progress)
        if current_state[PHEV] != 0:
            self.car_costs[PHEV] *= current_state[PHEV] ** (
                -self.technological_progress
            )
