print("GOV to do!")

class Abstract_Government:
    def __init__(self, energy_factor=1) -> None:
        raise Exception("")

    def get_subsidy(self, c_type) -> int:
        raise Exception("")

    def get_subsidy_val(self, c_type) -> int:
        raise Exception("")

    def update(self):
        raise Exception("")


class Government_Build_ChargingStation(Abstract_Government):
    def __init__(self, energy_factor=1) -> None:
        self.energy_factor = energy_factor
        self.society = None

    def set_society(self, society) -> None:
        self.society = society

    def get_subsidy(self, c_type) -> int:
        return 0

    def get_subsidy_val(self, c_type) -> int:
        return 0

    def update(self):
        self.society.city.build_new(1000)
