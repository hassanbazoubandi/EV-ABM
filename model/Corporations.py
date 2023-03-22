from networkx import network

class Corporations:
    def __init__(self, society: network) -> None:
        self.society = society
        pass

    @property
    def CV_price(self):
        return 10
    
    @property
    def PHEV_price(self):
        return 10

    @property
    def BEV_price(self):
        return 10
    
    def update():
        pass