import networkx as nx

from .Cars import Car, Car_CV, Car_BEV, Car_PHEV
from .Goverment import Goverment
from .Corporations import Corporations

class Society(nx.random_graphs.watts_strogatz_graph):
    CUSTOMER = "customer"
    def __init__(self, *args) -> None:
        super().__init__(*args)
        for node in self.nodes:
            self.nodes[node][Society.CUSTOMER] = Customer(
                self,
                node,
                self._get_initial_car(),
            )
        self.customers = [node[Society.CUSTOMER] for node in self.nodes]
        self.goverment = Goverment()
        self.corporations = Corporations()

    def _get_initial_car(self): #? stan początkowy aut
        return Car_CV()

    def customer(self, n: int):
        return self.nodes[n][Society.CUSTOMER]

    def _EV_cost_effective(self) -> bool: #? czy EV są opłacalne
        return True

    def go(self, N: int):
        for i in range(N):
            self._go(i)

    def _go(self, k: int):
        cost_effective = self._EV_cost_effective()
        for customer in self.customers:
            if customer.have_working_car(k):
                continue
            if cost_effective:
                # TOPSOS EV-PHEV
                pass
            elif self.public_charging_nerby(customer) and customer.environmental_attiude() and self.technological_innovator():
                customer.car = Car_BEV(k)
            else:
                # TOPSOS PHEV-CV
                pass
        self.corporations.update()
        self.goverment.update()


class Customer:
    def __init__(self, society: nx.network, number: int, car: Car, *args) -> None:
        self.society = society
        self.number = number
        self.car = car

    def have_working_car(self, year: int):
        return self.car.is_operational(year)

