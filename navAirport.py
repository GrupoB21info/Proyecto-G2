from navPoint import NavPoint

class NavAirport:
    def __init__(self, name, sids, stars):
        self.name = name
        self.sids = sids  # Lista de puntos de salida
        self.stars = stars  # Lista de puntos de llegada

    def __repr__(self):
        return f"NavAirport({self.name}, SIDs: {self.sids}, STARs: {self.stars})"



