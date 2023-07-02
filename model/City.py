"""
The city creates the environment of the model.
City is responsible for set initial public chargers,
add new, remove old and count all nearby to checked Customer.
"""
from typing import Tuple

import numpy as np

from .Customer import Customer


class City:
    """
    City manages chargers in the model
    """

    def __init__(self, city_size: Tuple[int, int], initial_chargers: int) -> None:
        """City manages chargers in the model.

        Args:
            city_size (Tuple[int, int]): City sizes. Model assume rectangle city.
            initial_chargers (int): Count of initial chargers.
        """
        self.charger_pos: np.ndarray | None = np.random.random(
            2 * initial_chargers
        ).reshape((initial_chargers, 2))
        self.city_size = city_size
        self.charger_pos[:, 0] = self.charger_pos[:, 0] * city_size[0]
        self.charger_pos[:, 1] = self.charger_pos[:, 1] * city_size[1]

    def count_nerby_chargers(self, customer: Customer, radius: float) -> int:
        """Get number of charges in radius of customer home.

        Args:
            customer (Customer): Customer to count chargers near him
            radius (float): If a charger is within a radius of the customer, it is considered a charger nearby.

        Returns:
            int: Number of loaders near the customer.
        """
        pos = np.array(customer.home)
        return (((self.charger_pos - pos) ** 2).sum(1) < radius**2).sum()

    def build_new(self, new_chargers: int):
        """Build new chargers.

        Args:
            new_chargers (int): Number of new chargers to build.
        """
        new_charges_pos = np.random.random(2 * new_chargers).reshape((new_chargers, 2))
        new_charges_pos[:, 0] = new_charges_pos[:, 0] * self.city_size[0]
        new_charges_pos[:, 1] = new_charges_pos[:, 1] * self.city_size[1]
        if self.charger_pos is None:
            self.charger_pos = new_charges_pos
        else:
            self.charger_pos = np.concatenate([self.charger_pos, new_charges_pos])

    def count_chargers(self) -> int:
        """Get number of public chargers

        Returns:
            int: Number of public chargers.
        """
        if self.charger_pos is None:
            return 0
        return self.charger_pos.shape[0]

    def close_charger(self, charger_number: int):
        """Close n-th public charger.

        Args:
            charger_number (int): Position charger to close.
        """
        if self.charger_pos is None:
            return
        if charger_number == 0 and self.count_chargers() == 1:
            self.charger_pos = None
        else:
            self.charger_pos = np.delete(self.charger_pos, charger_number, axis=0)
