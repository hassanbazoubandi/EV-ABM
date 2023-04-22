from .constants import CV, EV, PHEV


class Car:
    def __init__(self, release_year) -> None:
        self.release_year = release_year
        pass

    def is_operational(self, year: int) -> bool:
        return year - self.release_year < self.lifetime

    @property
    def lifetime(self):
        raise Exception("")

    @property
    def car_type(self):
        raise Exception("")


class Car_EV(Car):
    @property
    def lifetime(self):
        return 3

    @property
    def car_type(self):
        return EV


class Car_CV(Car):
    @property
    def lifetime(self):
        return 10

    @property
    def car_type(self):
        return CV


class Car_PHEV(Car):
    @property
    def lifetime(self):
        return 5

    @property
    def car_type(self):
        return PHEV
