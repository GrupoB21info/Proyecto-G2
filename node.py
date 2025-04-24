import math

class Node:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

    def __repr__(self):
        return f"Node({self.name}, {self.x}, {self.y})"

def AddNeighbor(n1: Node, n2: Node) -> bool:
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def Distance(n1: Node, n2: Node) -> float:
    return math.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)