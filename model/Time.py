"""
Time is responsible for converting time from model time to real time.
This is especially true for variable fuel and energy prices
"""
from typing import Tuple


class Time:
    """
    Time is responsible for converting time from model time to real time.
    """    
    def __init__(self, year: int, month: int) -> None:
        """Set initial time in model.

        Args:
            year (int): initial year
            month (int): initial month
        """        
        self.year = year
        self.month = month

    def get_current_date(self, year: int, month: int) -> Tuple[int, int]:
        """
        Get the current date based on the model's start date and operation date

        Args:
            year (int): year of operation of the model
            month (int): month of operation of the model

        Returns:
            Tuple[int, int]: current date: (year, month)
        """        
        return (
            year + self.year + (month + self.month - 1) // 12,
            (month + self.month - 1) % 12 + 1,
        )
