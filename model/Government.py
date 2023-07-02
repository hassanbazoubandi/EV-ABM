"""
Government represent type of one model agent. 
Government are responsible for introduce seted government strategy.
Actually are implemented:
- GovernmentBuildChargingStation
- GovernmentProvidesSubsidies
- GovernmentMixedStrategy
- GovernmentNoSubsidies
- GovernmentCloseChargingStation
  
Any of them inherit for class AbstractGovernment (like abstract class).
To check other strategies it is advisable to create a corresponding class inheriting from A
"""
from random import random

from .constants import CV, EV, PHEV, CarTypes

DEFLAUT_ONE_SUB_LEVEL = 83_000
DEFLAUT_PHEV_SUB_SCALER = 0.1
DEFLAUT_YEAR_SUBS = 1_000_000
DEFLAUT_NEW_CHARGERS = 10


def _get_subsidy_val(
    budget: int,
    sub_val: int,
    car_type: CarTypes,
    EV_scalar: float = 1,
    PHEV_scalar: float = 1,
    CV_scalar: float = 0,
) -> int:
    """Function count subsidy value.
    If there is enough money in the budget, then subsidy value is returned.
    In other case is returned 0

    Args:
        budget (int): Money in the budget.
        sub_val (int): bassic subsidy value
        car_type (CarTypes): The type of car for which the subsidy is checked.
        EV_scalar (float, optional): Subsidity for EV is sub_val * EV_scalar. Defaults to 1.
        PHEV_scalar (float, optional): Subsidity for PHEV is sub_val * PHEV_scalar. Defaults to 1.
        CV_scalar (float, optional): Subsidity for CV is sub_val * CV_scalar. Defaults to 0.

    Returns:
        int: subsidy value
    """
    scalars = {
        EV: EV_scalar,
        PHEV: PHEV_scalar,
        CV: CV_scalar,
    }
    if budget < sub_val * scalars[car_type]:
        return 0
    return sub_val * scalars[car_type]


class AbstractGovernment:
    """Abstract class of government."""

    def __init__(self, **kwargs) -> None:
        self.society: None | type = None
        self.budget = 0
        raise Exception("")

    def set_society(self, society: "Society") -> None:  # noqa
        """
            Set society. Society field may be useful
            in updating changing Society state,
            e.g., building new public chargers.

        Args:
            society (Society): Society class
        """
        self.society = society

    def get_subsidy(self, c_type: CarTypes) -> int:
        """Method responsible for determining the value of subsidies and subtracting them from the budget.

        Args:
            c_type (CarTypes): car type BEV, PHEV or CV

        Returns:
            int: value of subsidy
        """
        subsidy_value = self.get_subsidy_val(c_type)
        self.budget -= subsidy_value
        return subsidy_value

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        """Method responsible for determining the value of subsidies.

        Args:
            c_type (CarTypes): car type BEV, PHEV or CV

        Returns:
            int: value of subsidy
        """
        raise Exception("")

    def update(self, current_month: int):
        """Method called at the end of each time step.

        Args:
            current_month (int): integer value with range from 0 to 11 inclusive.
        """
        raise Exception("")


class GovernmentNoSubsidies(AbstractGovernment):
    """This class extend AbstractGovernment for model
    This class represent base scenario where government does not give subsidies.
    """

    def __init__(self, **kwargs) -> None:
        self.society: None | type = None

    def get_subsidy(self, c_type: CarTypes) -> int:
        return 0

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        """Method responsible for determining the value of subsidies.
        In this scenario always 0.

        Args:
            c_type (CarTypes): car type BEV, PHEV or CV

        Returns:
            int: value of subsidy
        """
        return 0

    def update(self, current_month: int):
        """Method called at the end of each time step.
        In this scenario do nothing.

        Args:
            current_month (int): integer value with range from 0 to 11 inclusive.
        """
        pass


class GovernmentBuildChargingStation(AbstractGovernment):
    """This class extend AbstractGovernment for model
    This class represent pure scenario where government build charging stations.
    """

    def __init__(self, *, new_chargers: int = DEFLAUT_NEW_CHARGERS) -> None:
        self.new_chargers = new_chargers
        self.society = None

    def get_subsidy(self, c_type: CarTypes) -> int:
        return 0

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        """Method responsible for determining the value of subsidies.
        In this scenario always 0.

        Args:
            c_type (CarTypes): car type BEV, PHEV or CV

        Returns:
            int: value of subsidy
        """
        return 0

    def update(self, current_month: int):
        """Method called at the end of each time step.
        In this scenario build new charging stations in city.

        Args:
            current_month (int): integer value with range from 0 to 11 inclusive.
        """
        if current_month:
            return
        self.society.city.build_new(self.new_chargers)


class GovernmentProvidesSubsidies(AbstractGovernment):
    """This class extend AbstractGovernment for model
    This class represent pure scenario where government gives subsidy.
    """

    def __init__(
        self,
        *,
        one_subsidy_level: int = DEFLAUT_ONE_SUB_LEVEL,
        year_subsidies: int = DEFLAUT_YEAR_SUBS,
        PHEV_sub_scaler: float = DEFLAUT_PHEV_SUB_SCALER,
    ) -> None:
        self.year_subsidies = year_subsidies
        self.PHEV_sub_scaler = PHEV_sub_scaler
        self.one_subsidy_level = one_subsidy_level
        self.budget = year_subsidies
        self.society = None

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        """Method responsible for determining the value of subsidies.

        Args:
            c_type (CarTypes): car type BEV, PHEV or CV

        Returns:
            int: value of subsidy
        """
        return _get_subsidy_val(
            self.budget, self.one_subsidy_level, c_type, 1, self.PHEV_sub_scaler, 0
        )

    def update(self, current_month: int):
        """Method called at the end of each time step.
        In this scenario renews budget.

        Args:
            current_month (int): integer value with range from 0 to 11 inclusive.
        """
        if current_month:
            return
        self.budget = self.year_subsidies


class GovernmentMixedStrategy(AbstractGovernment):
    """This class extend AbstractGovernment for model
    This class represent mixed scenario where government both gives subsidy and build charging stations.
    By default half subsidy budget and build half count of new charging stations compared to pure strategies.
    """

    def __init__(
        self,
        *,
        one_subsidy_level: int = DEFLAUT_ONE_SUB_LEVEL,
        year_subsidies: int = DEFLAUT_YEAR_SUBS // 2,
        new_chargers: int = DEFLAUT_NEW_CHARGERS // 2,
        PHEV_sub_scaler: float = DEFLAUT_PHEV_SUB_SCALER,
    ) -> None:
        self.PHEV_sub_scaler = PHEV_sub_scaler
        self.year_subsidies = year_subsidies
        self.one_subsidy_level = one_subsidy_level
        self.new_chargers = new_chargers
        self.budget = year_subsidies
        self.society = None

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        """Method responsible for determining the value of subsidies.

        Args:
            c_type (CarTypes): car type BEV, PHEV or CV

        Returns:
            int: value of subsidy
        """
        return _get_subsidy_val(
            self.budget, self.one_subsidy_level, c_type, 1, self.PHEV_sub_scaler, 0
        )

    def update(self, current_month: int):
        """Method called at the end of each time step.
        In this scenario renews budget and build new charging stations in city.

        Args:
            current_month (int): integer value with range from 0 to 11 inclusive.
        """
        if current_month:
            return
        self.budget = self.year_subsidies
        self.society.city.build_new(self.new_chargers)


class GovernmentCloseChargingStation(AbstractGovernment):
    """This class extend AbstractGovernment for model
    This class represent scenario where government close charging stations.
    """

    def __init__(self, *, closing_factor: float = 0.6) -> None:
        self.closing_factor = closing_factor
        self.society = None

    def get_subsidy_val(self, c_type: CarTypes) -> int:
        """Method responsible for determining the value of subsidies.
        In this scenario always 0.
        Args:
            c_type (CarTypes): car type BEV, PHEV or CV.

        Returns:
            int: value of subsidy
        """
        return 0

    def update(self, current_month: int):
        """Method called at the end of each time step.
        In this scenario close charging stations in city, any with closing_factor probability.

        Args:
            current_month (int): integer value with range from 0 to 11 inclusive.
        """
        if current_month:
            return
        for i in range(self.society.city.count_chargers() - 1, 0, -1):
            if random() < self.closing_factor:
                self.society.city.close_charger(i)
