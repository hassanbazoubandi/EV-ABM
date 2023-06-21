import json
import os
from random import random
from typing import Callable, Dict, List, Tuple

import pandas as pd

from .Cars import Car, Car_CV, Car_EV, Car_PHEV
from .City import City
from .common import get_data, get_initial_params
from .constants import CV, EV, PHEV, CarTypes
from .Corporations import Corporations
from .Customer import Customer
from .Government import AbstractGovernment
from .Prices import ConstatntPrice, Price, Prices
from .Time import Time

initial_params = get_initial_params()
data = get_data()
car_params = data["cars"]
customers_params = data["customers"]

car_types = [EV, PHEV, CV]


class Society:
    def __init__(
        self,
        population: int,
        alpha: float,
        government: AbstractGovernment,
        corporation_margin: float,
        corporation_technological_progress: float,
        city_size: Tuple[int, int],
        nerby_radius: float,
        initial_public_chargers: int,
        energy_factor: float,
        *,
        car_price_noise: None | Callable[[], float],
        **kwargs,
    ) -> None:
        if alpha < 0 or alpha > 1:
            raise ValueError("alpha parameter have to be float in [0, 1] interval")
        if energy_factor < 0 or energy_factor > 1:
            raise ValueError(
                "energy_factor parameter have to be float in [0, 1] interval"
            )
        self.energy_factor = (1 + energy_factor**2) / (1 + energy_factor)
        self.alpha = alpha
        self.nerby_radius = nerby_radius
        if car_price_noise is None:
            self.car_price_noise = lambda: 0.0
        else:
            self.car_price_noise = car_price_noise

        self.customers: List[Customer] = []
        for _ in range(population):
            self.customers.append(
                Customer(
                    self,
                    self._get_initial_car(),
                    self._get_initial_profile(),
                    city_size,
                )
            )

        self.government = government
        self.government.set_society(self)

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

    def _set_states(self) -> None:
        self.state[CV] = 0
        self.state[PHEV] = 0
        self.state[EV] = 0
        for customer in self.customers:
            self.state[customer.get_car_type()] += 1
        self.historical_states.append(self.state.copy())

    def get_historical_states(self) -> pd.DataFrame:
        df_historical_data = pd.DataFrame(self.historical_states)
        df_historical_data["year"] = df_historical_data.index
        return df_historical_data

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

    def _get_annual_cost(
        self, customer: Customer, year: int, month: int
    ) -> Dict[CarTypes, float]:
        cost: Dict[CarTypes, float] = {}
        for c_type in car_types:
            cost[c_type] = self.corporations.get_price(
                c_type
            ) - self.government.get_subsidy_val(c_type)

        cost[CV] += (
            float(customers_params["profiles"][customer.profile]["mean"])
            * Car_CV.cost_per_km(
                *self.time.get_current_date(year, month), fuel_price=self.fuel_price
            )
            * int(car_params[CV]["lifetime"])
        )

        cost[PHEV] += (
            float(customers_params["profiles"][customer.profile]["mean"])
            * Car_PHEV.cost_per_km(
                *self.time.get_current_date(year, month),
                energy_factor=self.energy_factor,
                energy_price=self.energy_price,
                fuel_price=self.fuel_price,
            )
            * int(car_params[PHEV]["lifetime"])
        )

        cost[EV] += (
            float(customers_params["profiles"][customer.profile]["mean"])
            * Car_EV.cost_per_km(
                *self.time.get_current_date(year, month),
                energy_factor=self.energy_factor,
                energy_price=self.energy_price,
            )
            * int(car_params[EV]["lifetime"])
        )

        for c_type in car_types:
            cost[c_type] /= int(car_params[c_type]["lifetime"])
            if cost[c_type] < 0:
                print(f"Woops! In this case annual cost of {c_type} is smaller then 0.")
            cost[c_type] = max(0, cost[c_type] + self.car_price_noise())
        return cost

    def public_charging_nerby(self, customer: Customer) -> bool:
        return self.city.count_nerby_chargers(customer, self.nerby_radius) > 0

    def run(self, n_steps: int) -> None:
        for i in range(1, n_steps + 1):
            current_year = i // 12
            current_month = i % 12
            self._set_states()
            self._run(current_year, current_month)
            self.corporations.update(self.historical_states[-1], current_month)
            self.government.update(current_month)
        self._set_states()

    def _run(self, current_year: int, current_month: int) -> None:
        for customer in self.customers:
            if customer.have_working_car(current_year, current_month):
                continue
            annual_cost = self._get_annual_cost(customer, current_year, current_month)
            if annual_cost[EV] == min(annual_cost.values()):
                customer.buy(EV, current_year, current_month)
                continue
            if annual_cost[PHEV] == min(annual_cost.values()):
                customer.buy(PHEV, current_year, current_month)
                continue
            if self.public_charging_nerby(customer):
                if random() < self.alpha:
                    customer.buy(EV, current_year, current_month)
                    continue
                customer.choose(CV, PHEV, current_year, current_month)
                continue
            customer.buy(CV, current_year, current_month)


class SocietyVariableEnergyPrices(Society):
    def __init__(
        self,
        population: int,
        alpha: float,
        government: AbstractGovernment,
        corporation_margin: float,
        corporation_technological_progress: float,
        city_size: Tuple[int, int],
        nerby_radius: float,
        initial_public_chargers: int,
        energy_factor: float,
        *,
        car_price_noise: None | Callable[[], float],
        initial_time: Tuple[int, int]=(0,0),
        energy_prices_csv: str = "",
        fuel_prices_csv: str = "",
        **kwargs,
    ) -> None:
        super().__init__(population, alpha, government, corporation_margin, corporation_technological_progress, city_size, nerby_radius, initial_public_chargers, energy_factor, car_price_noise=car_price_noise, **kwargs)
        self.time = Time(initial_time)
        self.energy_price: Price = Prices(energy_prices_csv)
        self.fuel_price: Price = Prices(fuel_prices_csv)


class SocietyConstantsEnergyPrices(Society):
    def __init__(
        self,
        population: int,
        alpha: float,
        government: AbstractGovernment,
        corporation_margin: float,
        corporation_technological_progress: float,
        city_size: Tuple[int, int],
        nerby_radius: float,
        initial_public_chargers: int,
        *,
        energy_price: float = 0,
        fuel_price: float = 0,
        car_price_noise: None | Callable[[], float],
        **kwargs,
    ) -> None:
        super().__init__(
            population,
            alpha,
            government,
            corporation_margin,
            corporation_technological_progress,
            city_size,
            nerby_radius,
            initial_public_chargers,
            car_price_noise=car_price_noise,
            **kwargs,
        )
        self.time = Time(0, 0)
        self.energy_price = ConstatntPrice(energy_price)
        self.fuel_price = ConstatntPrice(fuel_price)
