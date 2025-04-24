from node import *

class Segment:
    def __init__(self, name: str, origin: Node, destination: Node):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)

    def __repr__(self):
        return f"Segment({self.name}, de {self.origin.name} hasta {self.destination.name}, Cost: {self.cost})"
