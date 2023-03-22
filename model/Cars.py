class Car:
    def __init__(self, release_year) -> None:
        self.release_year = release_year
        pass
    
    def is_operational(self, year: int) -> bool:
        return year - self.release_year < self.lifetime

    @property
    def lifetime(self):
        raise Exception("")

class Car_BEV(Car):
    @property
    def lifetime(self):
        return 3

class Car_CV(Car):
    @property
    def lifetime(self):
        return 10

class Car_PHEV(Car):
    @property
    def lifetime(self):
        return 5
