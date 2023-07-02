"""
Cars, as a customer field, are responsible for type (BEV, PHEV, CV),
age and cost per km.
Any car type has own class witch inherit for class Car (like abstract class).
"""
from random import randint

from .common import get_data
from .constants import CV, EV, PHEV, CarTypes

data = get_data()
car_params = data["cars"]


class Car:
    """Like abstract class for car from model."""

    def __init__(
        self, release_year: int | None = None, release_month: int | None = None
    ) -> None:
        """Like abstract class for car from model.
        In this class are both possibility.
        If release_year or release_month are None, then they are drawn randomly.
        Args:
            release_year (int | None, optional): Year of release of the car. Defaults to None.
            release_month (int | None, optional): Month of release of the car. From 0 to 11. Defaults to None.
        """
        if release_year is None:
            release_year = -randint(0, self.lifetime)
        if release_month is None:
            release_month = randint(0, 11)
        self.release_year = release_year
        self.release_month = release_month

    def is_operational(self, year: int, month: int) -> bool:
        """This method compare actual car are and them lifetime.
        Car is operational if his age < lifetime.

        Args:
            year (int): Current year.
            month (int): Current month.

        Returns:
            bool: True if car is operational (age < lifetime), False in other case.
        """
        return (
            year - self.release_year + (month - self.release_month) / 12 < self.lifetime
        )

    def age(self, year: int, month: int) -> float:
        """Get current age of car.

        Args:
            year (int): Current year.
            month (int): Current month.

        Returns:
            float: Age of the car in years.
        """
        return year - self.release_year + (month - self.release_month) / 12

    @property
    def lifetime(self) -> int:
        """Get car lifetime.
        Lifetime is get from data.json
        valid_json[self.car_type]["lifetime"]

        Returns:
            int: Car lifetime.
        """
        return car_params[self.car_type]["lifetime"]

    @property
    def car_type(self) -> CarTypes:
        """Get car type.

        Returns:
            CarTypes: Car type.
        """
        raise Exception("")

    @staticmethod
    def cost_per_km(year: int, month: int, **kwargs) -> float:
        """Get cost per km.
        cost_per_km = (consumption_per_100km * resource_price) / 100

        Args:
            year (int): Current year.
            month (int): Current month.

        Returns:
            float: Return cost per km.
        """
        raise Exception("")


class Car_CV(Car):
    @property
    def car_type(self) -> CarTypes:
        """Get car type.

        Returns:
            CarTypes: CV
        """
        return CV

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        """Get cost per km.
        cost_per_km = (consumption_per_100km * resource_price) / 100

        Args:
            year (int): Current year.
            month (int): Current month.

        Returns:
            float: Return cost per km.
        """
        return (
            car_params[CV]["fuel_consumption"]
            * kwargs["fuel_price"].get_price(year, month)
            / 100
        )


class Car_PHEV(Car):
    @property
    def car_type(self) -> CarTypes:
        """Get car type.

        Returns:
            CarTypes: PHEV
        """
        return PHEV

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        """Get cost per km.
        cost_per_km = (consumption_per_100km * resource_price) / 100
        By deflaut energy consumption is in kWh, but energy price in MWh.

        Args:
            year (int): Current year.
            month (int): Current month.
        Kwargs:
            energy_factor (float):

        Returns:
            float: Return cost per km.
        """
        return (
            kwargs["energy_factor"]
            * car_params[PHEV]["energy_consumption"]
            * kwargs["energy_price"].get_price(year, month)
            / 1000  # energy consumption in kWh, energy price in MWh
            + car_params[PHEV]["fuel_consumption"]
            * kwargs["fuel_price"].get_price(year, month)
        ) / 200


class Car_EV(Car):
    @property
    def car_type(self) -> CarTypes:
        """Get car type.

        Returns:
            CarTypes: EV
        """
        return EV

    @staticmethod
    def cost_per_km(year, month, **kwargs) -> float:
        """Get cost per km.
        cost_per_km = (consumption_per_100km * resource_price) / 100
        By deflaut energy consumption is in kWh, but energy price in MWh.

        Args:
            year (int): Current year.
            month (int): Current month.
        Kwargs:
            energy_factor (float): Energy price scalar.

        Returns:
            float: Return cost per km.
        """
        return (
            kwargs["energy_factor"]
            * car_params[EV]["energy_consumption"]
            * kwargs["energy_price"].get_price(year, month)
            / (100 * 1000)  # energy consumption in kWh, energy price in MWh
        )
