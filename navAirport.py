from navPoint import NavPoint

class NavAirport:
    def __init__(self, name, sids, stars):
        self.name = name
        self.sids = sids
        self.stars = stars

    def __repr__(self):
        return f"NavAirport({self.name}, SIDs: {self.sids}, STARs: {self.stars})"



