class Goverment:
    def __init__(self, society, energy_factor=1) -> None:
        print("GOV to do!")
        self.society = society
        self.energy_factor = energy_factor

    def get_subsidy(self, c_type) -> int:
        return 1

    def get_subsidy_val(self, c_type) -> int:
        return 1

    def update(self):
        pass
