from random import randint, random
from typing import Tuple

import pandas as pd

from .Cars import Car, Car_CV, Car_EV, Car_PHEV
from .City import City
from .constants import CV, EV, PHEV, oc_h, oc_p, year_bev
from .Corporations import Corporations
from .Custormer import Customer
from .Goverment import Goverment


class Society:
    def __init__(
        self,
        population,
        alpha: float,
        corporation_margin: float,
        corporation_technological_progress: float,
        city_size: Tuple[int, int],
        nerby_radius: float,
        initial_public_chargers: int,
    ) -> None:
        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha parameter have to be float in [0, 1] interval")
        self.alpha = alpha
        self.customers = []
        self.nerby_radius = nerby_radius
        for _ in range(population):
            self.customers.append(
                Customer(
                    self._get_initial_car(),
                    self._get_initial_procfile(),
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
        self.historical_states = []

    def _get_initial_procfile(self):
        return random() < 0.5 if 1 else 0

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

    def _get_initial_car(self) -> Car:  # ? stan początkowy aut
        # TODO sprawdzić rozkład
        return Car_CV(release_year=-randint(0, 10))

    def _EV_cost_effective(self) -> bool:  # ? czy EV są opłacalne
        # return True
        c_bev = self.corporations.EV_price
        c_cv = self.corporations.CV_price
        s_bev = self.goverment.get_subsidy_val()
        rc_h = oc_h / (oc_h + oc_p)
        rc_p = 1 - rc_h
        sav_bev = rc_h * oc_h + rc_p * oc_p
        pre_bev = c_bev - s_bev - c_cv
        ce = pre_bev - sav_bev * year_bev
        return ce < 0

    def public_charging_nerby(self, customer: Customer) -> bool:
        return self.city.is_nerby(customer, self.nerby_radius) > 0

    def go(self, N: int):
        for i in range(1, N + 1):
            self._set_states()
            self._go(i)
        self._set_states()
        self.corporations.update(self.historical_states[-1])
        self.goverment.update()

    def _go(self, current_year: int):
        for customer in self.customers:
            if customer.have_working_car(current_year):
                continue
            cost_effective = self._EV_cost_effective()
            if cost_effective == EV:
                customer.buy(EV, current_year)
                continue
            if cost_effective == PHEV:
                customer.buy(PHEV, current_year)
                continue
            if self.public_charging_nerby(customer,self.nerby_radius):
                if self.alpha < random():
                    customer.buy(EV, current_year)
                    continue
                customer.choose(CV, PHEV, current_year)
            customer.buy(CV, current_year)
