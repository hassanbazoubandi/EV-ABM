from .constants import CV, EV, PHEV


class Corporations:
    def __init__(self, margin, technological_progress) -> None:
        self.margin = margin
        self.technological_progress = technological_progress
        self.car_costs = {
            CV: 60_000,
            EV: 120_000,
            PHEV: 100_000,
        }

    @property
    def CV_price(self):
        return (1 + self.margin) * self.car_costs[CV]

    @property
    def PHEV_price(self):
        return (1 + self.margin) * self.car_costs[PHEV]

    @property
    def EV_price(self):
        return (1 + self.margin) * self.car_costs[EV]

    def update(self, current_state):  # TODO do poprawy
        if current_state[EV] != 0:
            self.car_costs[EV] *= current_state[EV] ** (-self.technological_progress)
        if current_state[PHEV] != 0:
            self.car_costs[PHEV] *= current_state[PHEV] ** (
                -self.technological_progress
            )
