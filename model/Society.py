import json
from random import random
from typing import Dict, List, Tuple

import pandas as pd

from .Cars import Car, Car_CV, Car_EV, Car_PHEV
from .City import City
from .constants import CV, EV, PHEV, CarTypes
from .Corporations import Corporations
from .Customer import Customer
from .Goverment import Goverment
from .Time import Time

with open("model/initial_params.json", "r") as plik:
    initial_params = json.load(plik)

with open("model/data.json", "r") as plik:
    data = json.load(plik)
    car_params = data["cars"]
    customers_params = data["customers"]

car_types = [EV, PHEV, CV]


class Society:
    def __init__(
        self,
        population: int,
        alpha: float,
        corporation_margin: float,
        corporation_technological_progress: float,
        city_size: Tuple[int, int],
        nerby_radius: float,
        initial_public_chargers: int,
        initial_time: Tuple[int, int],
    ) -> None:
        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha parameter have to be float in [0, 1] interval")
        self.time = Time(*initial_time)
        self.alpha = alpha
        self.customers: List[Customer] = []
        self.nerby_radius = nerby_radius
        for _ in range(population):
            self.customers.append(
                Customer(
                    self._get_initial_car(),
                    self._get_initial_profile(),
                    city_size,
                )
            )
        self.goverment = Goverment(None)
        self.corporations = Corporations(
            corporation_margin, corporation_technological_progress
        )
        self.city = City(city_size, initial_public_chargers)
        self.state = {
            CV: 0,
            PHEV: 0,
            EV: 0,
        }
        self.historical_states: List[Dict[CarTypes, int]] = []

    def _get_initial_profile(self) -> CarTypes:
        rdm = random()
        if rdm < initial_params["profiles_distribution"][CV]:
            return CV
        if (
            rdm
            < initial_params["profiles_distribution"][CV]
            + initial_params["profiles_distribution"][PHEV]
        ):
            return PHEV
        return EV

    def _set_states(self):
        self.state[CV] = 0
        self.state[PHEV] = 0
        self.state[EV] = 0
        for customer in self.customers:
            self.state[customer.get_car_type()] += 1
        self.historical_states.append(self.state.copy())

    def get_historical_states(self):
        df = pd.DataFrame(self.historical_states)
        df["year"] = df.index
        return df

    def _get_initial_car(self) -> Car:
        rdm = random()
        if rdm < initial_params["car_distribution"][CV]:
            return Car_CV()
        if (
            rdm
            < initial_params["car_distribution"][CV]
            + initial_params["car_distribution"][PHEV]
        ):
            return Car_PHEV()
        return Car_EV()

    def _get_annual_cost(self, customer, year, month) -> Dict[CarTypes, float]:
        cost: Dict[CarTypes, float] = {}
        for c_type in car_types:
            cost[c_type] = self.corporations.get_price(
                c_type
            ) - self.goverment.get_subsidy_val(c_type)

        cost[CV] += (
            customers_params["profiles"][customer.profile]["mean"]
            * Car_CV.cost_per_km(*self.time.get_current_date(year, month))
            * car_params[CV]["lifetime"]
        )
        cost[PHEV] += (
            customers_params["profiles"][customer.profile]["mean"]
            * Car_PHEV.cost_per_km(
                *self.time.get_current_date(year, month),
                energy_factor=self.goverment.energy_factor
            )
            * car_params[PHEV]["lifetime"]
        )
        cost[EV] += (
            customers_params["profiles"][customer.profile]["mean"]
            * Car_EV.cost_per_km(
                *self.time.get_current_date(year, month),
                energy_factor=self.goverment.energy_factor
            )
            * car_params[EV]["lifetime"]
        )
        for c_type in car_types:
            cost[c_type] /= car_params[c_type]["lifetime"]
        return cost

    def public_charging_nerby(self, customer: Customer) -> bool:
        return self.city.count_nerby_chargers(customer, self.nerby_radius) > 0

    def go(self, N: int):
        for i in range(1, N + 1):
            self._set_states()
            self._go(i)
        self._set_states()
        self.corporations.update(self.historical_states[-1])
        self.goverment.update()

    def _go(self, step: int):
        current_year = step // 12
        current_month = step % 12
        for customer in self.customers:
            if customer.have_working_car(current_year, current_month):
                continue
            annual_cost = self._get_annual_cost(customer, current_month, current_year)
            if annual_cost[EV] == min(annual_cost.values()):
                customer.buy(EV, current_year, current_month)
                continue
            if annual_cost[PHEV] == min(annual_cost.values()):
                customer.buy(PHEV, current_year, current_month)
                continue
            if self.public_charging_nerby(customer):
                if self.alpha < random():
                    customer.buy(EV, current_year, current_month)
                    continue
                customer.choose(CV, PHEV, current_year, current_month)
            customer.buy(CV, current_year, current_month)
