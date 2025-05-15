from navPoint import NavPoint

class NavSegment:
    def __init__(self, origin: NavPoint, destination: NavPoint, distance: float):
        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __repr__(self):
        return f"NavSegment({self.origin.name} -> {self.destination.name}, {self.distance} km)"
