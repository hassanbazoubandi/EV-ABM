from random import random
from typing import Type

from .constants import CV, EV, PHEV, CarTypes


class AbstractGovernment:
    def __init__(self, **kwargs) -> None:
        self.society = None
        raise Exception("")

    def set_society(self, society: type) -> None:
        self.society = society

    def get_subsidy(self, c_type: CarTypes) -> int:
        raise Exception("")

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        raise Exception("")

    def update(self, current_month: int):
        raise Exception("")


class GovernmentBuildChargingStation(AbstractGovernment):
    def __init__(self, *, new_chargers=20) -> None:
        self.new_chargers = new_chargers
        self.society = None

    def get_subsidy(self, c_type: CarTypes) -> int:
        return 0

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        return 0

    def update(self, current_month: int):
        if current_month:
            return
        self.society.city.build_new(self.new_chargers)


class GovernmentProvidesSubsidies(AbstractGovernment):
    def __init__(self, *, one_subsidity_level=30_000, year_subsidies=10**6, PHEV_sub_scaler = 1) -> None:
        self.year_subsidies = year_subsidies
        self.PHEV_sub_scaler = PHEV_sub_scaler
        self.one_subsidity_level = one_subsidity_level
        self.budget = year_subsidies
        self.society = None

    def get_subsidy(self, c_type: CarTypes) -> int:
        sub = self.get_subsidy_val(c_type)
        self.budget -= sub
        return sub

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        if c_type == EV:
            return (
                self.one_subsidity_level
                if self.one_subsidity_level > self.budget
                else 0
            )
        if c_type == PHEV:
            return (
                self.one_subsidity_level * self.PHEV_sub_scaler
                if self.one_subsidity_level * self.PHEV_sub_scaler > self.budget
                else 0
            )
        return 0

    def update(self, current_month: int):
        if current_month:
            return
        self.budget = self.year_subsidies


class GovernmentMixedStrategy(AbstractGovernment):
    def __init__(
        self, *, one_subsidity_level=30_000, year_subsidies=5e5, new_chargers=10, PHEV_sub_scaler = 1
    ) -> None:
        self.PHEV_sub_scaler = PHEV_sub_scaler
        self.year_subsidies = year_subsidies
        self.one_subsidity_level = one_subsidity_level
        self.new_chargers = new_chargers
        self.budget = year_subsidies
        self.society = None


    def get_subsidy(self, c_type: CarTypes) -> int:
        sub = self.get_subsidy_val(c_type)
        self.budget -= sub
        return sub

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        if c_type == EV:
            return (
                self.one_subsidity_level
                if self.one_subsidity_level > self.budget
                else 0
            )
        if c_type == PHEV:
            return (
                self.one_subsidity_level * self.PHEV_sub_scaler
                if self.one_subsidity_level * self.PHEV_sub_scaler > self.budget
                else 0
            )
        return 0

    def update(self, current_month: int):
        if current_month:
            return
        self.budget = self.year_subsidies
        self.society.city.build_new(self.new_chargers)


class GovernmentCloseChargingStation(AbstractGovernment):
    def __init__(self, *, closing_factor=0.6) -> None:
        self.closing_factor = closing_factor
        self.society = None

    def get_subsidy(self, c_type: CarTypes) -> int:
        return 0

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        return 0

    def update(self, current_month: int):
        if current_month:
            return
        for i in range(self.society.city.count_chargers() - 1, 0, -1):
            if random() < self.closing_factor:
                self.society.city.close_charger(i)
