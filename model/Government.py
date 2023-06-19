from random import random

from .constants import CV, EV, PHEV, CarTypes

DEFLAUT_ONE_SUB_LEVEL = 83_000
DEFLAUT_PHEV_SUB_SCALER = 0.1
DEFLAUT_YEAR_SUBS = 1_000_000
DEFLAUT_NEW_CHARGERS = 10


def _get_subsidity_val(
    budget: int,
    sub_val: int,
    car_type: CarTypes,
    EV_scalar: float = 1,
    PHEV_scalar: float = 1,
    CV_scalar: float = 0,
):
    scalars = {
        EV: EV_scalar,
        PHEV: PHEV_scalar,
        CV: CV_scalar,
    }
    if budget < sub_val * scalars[car_type]:
        return 0
    return sub_val * scalars[car_type]


class AbstractGovernment:
    def __init__(self, **kwargs) -> None:
        self.society: None | type = None
        raise Exception("")

    def set_society(self, society: "Society") -> None:  # noqa
        self.society = society

    def get_subsidy(self, c_type: CarTypes) -> int:
        raise Exception("")

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        raise Exception("")

    def update(self, current_month: int):
        raise Exception("")



class GovernmentNoSubsidies(AbstractGovernment):
    def __init__(self, **kwargs) -> None:
        self.society: None | type = None

    def set_society(self, society: "Society") -> None:  # noqa
        self.society = society

    def get_subsidy(self, c_type: CarTypes) -> int:
        return 0

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        return 0

    def update(self, current_month: int):
        pass


class GovernmentBuildChargingStation(AbstractGovernment):
    def __init__(self, *, new_chargers: int = DEFLAUT_NEW_CHARGERS) -> None:
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
    def __init__(
        self,
        *,
        one_subsidity_level: int = DEFLAUT_ONE_SUB_LEVEL,
        year_subsidies: int = DEFLAUT_YEAR_SUBS,
        PHEV_sub_scaler: float = DEFLAUT_PHEV_SUB_SCALER,
    ) -> None:
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
        return _get_subsidity_val(
            self.budget, self.one_subsidity_level, c_type, 1, self.PHEV_sub_scaler, 0
        )

    def update(self, current_month: int):
        if current_month:
            return
        self.budget = self.year_subsidies


class GovernmentMixedStrategy(AbstractGovernment):
    def __init__(
        self,
        *,
        one_subsidity_level: int = DEFLAUT_ONE_SUB_LEVEL,
        year_subsidies: int = DEFLAUT_YEAR_SUBS // 2,
        new_chargers: int = DEFLAUT_NEW_CHARGERS // 2,
        PHEV_sub_scaler: float = DEFLAUT_PHEV_SUB_SCALER,
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
        return _get_subsidity_val(
            self.budget, self.one_subsidity_level, c_type, 1, self.PHEV_sub_scaler, 0
        )

    def update(self, current_month: int):
        if current_month:
            return
        self.budget = self.year_subsidies
        self.society.city.build_new(self.new_chargers)


class GovernmentCloseChargingStation(AbstractGovernment):
    def __init__(self, *, closing_factor: float = 0.6) -> None:
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
