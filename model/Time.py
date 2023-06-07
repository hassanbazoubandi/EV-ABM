from typing import Tuple


class Time:
    def __init__(self, year, month) -> None:
        self.year = year
        self.month = month

    def get_current_date(self, year, month) -> Tuple[int, int]:
        return (
            year + self.year + (month + self.month - 1) // 12,
            (month + self.month - 1) % 12 + 1,
        )
