"""
Corporation represent type of one model agent.
Corporations are responsible for auto prices and their changes.
Model assume technological progress which influence to electric cars cost decreases.
"""
from typing import Dict

from .common import get_data
from .constants import CV, EV, PHEV, CarTypes

data = get_data()
car_params = data["cars"]


def in_money(value: float) -> float:
    """Cut the value to two decimal places
    Represent value as currency.

    Args:
        value (float): Vlaue to cut.

    Returns:
        float: Cut value.
    """
    return int(value * 100) / 100


class Corporations:
    """
    Corporation is an agent of the model responsible for car cost changes.
    """

    def __init__(self, margin: float, technological_progress: float) -> None:
        """Corporation is an agent of the model responsible for car cost changes.
        Car prices are read from data.json, and price = valid_json[c_type]["cost"]

        Args:
            margin (float): Cost is counted with corporation margin.
            technological_progress (float): Parameter responsible for cost decreases.
        """
        self.margin = margin
        self.technological_progress = technological_progress
        self.car_costs: Dict[CarTypes, float] = {
            CV: car_params[CV]["cost"] / (1 + self.margin),
            EV: car_params[EV]["cost"] / (1 + self.margin),
            PHEV: car_params[PHEV]["cost"] / (1 + self.margin),
        }

    def get_price(self, c_type: CarTypes) -> float:
        """Get the current price of a c_type car.

        Args:
            c_type (CarTypes): Car type

        Returns:
            float: The current price of a c_type car.
        """
        return in_money((1 + self.margin) * self.car_costs[c_type])

    def update(self, current_state: Dict[CarTypes, int], current_month: int) -> None:
        """Method called at the end of each time step.

        Args:
            current_state (Dict[CarTypes, int]): Current numbers of different types of cars.
            current_month (int): integer value with range from 0 to 11 inclusive.
        """
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
