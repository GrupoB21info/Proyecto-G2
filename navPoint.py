class NavPoint:
    def __init__(self, number, name, lat, lon):
        self.number = number
        self.name = name
        self.lat = float(lat)
        self.lon = float(lon)
        self.neighbors = []

    def __repr__(self):
        return f"NavPoint({self.name}, {self.lat}, {self.lon})"

