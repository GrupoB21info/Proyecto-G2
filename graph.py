import matplotlib.pyplot as plt

from segment import *


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

def AddNode(g, n):
    if any(node.name == n.name for node in g.nodes):
        return False
    g.nodes.append(n)
    return True

def AddSegment(graph, name, origin_name, dest_name):
    """
    Crea un segmento entre dos nodos y los conecta como vecinos.
    """
    origin = next((n for n in graph.nodes if n.name == origin_name), None)
    dest = next((n for n in graph.nodes if n.name == dest_name), None)

    if origin and dest:
        # Crear el segmento
        segment = Segment(name, origin, dest)
        graph.segments.append(segment)

        # Conectar nodos como vecinos
        AddNeighbor(origin, dest)
        AddNeighbor(dest, origin)  # Bidireccional

        return True

    return False


def GetClosest(g, x, y):
    return min(g.nodes, key=lambda n: math.sqrt((n.x - x) ** 2 + (n.y - y) ** 2))

def Plot(g):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14, 10))
    plt.clf()

    for node in g.nodes:
        plt.plot(node.x, node.y, 'o', color='blue')
        plt.text(node.x + 0.1, node.y + 0.1, node.name, fontsize=7,
                 bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

    for s in g.segments:
        x_vals = [s.origin.x, s.destination.x]
        y_vals = [s.origin.y, s.destination.y]
        color = getattr(s, 'color', 'gray')
        plt.plot(x_vals, y_vals, color=color, linewidth=1)
        cx = (s.origin.x + s.destination.x) / 2
        cy = (s.origin.y + s.destination.y) / 2
        plt.text(cx, cy, f"{s.cost:.2f}", fontsize=6)


    if g.nodes:
        xs = [n.x for n in g.nodes]
        ys = [n.y for n in g.nodes]
        plt.xlim(min(xs) - 1, max(xs) + 1)
        plt.ylim(min(ys) - 1, max(ys) + 1)

    plt.title("Grafo")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(alpha=0.3)

    return plt.gcf()

def PlotNode(g, name):
    plt.figure(figsize=(14, 10))
    plt.clf()
    node = next((n for n in g.nodes if n.name == name), None)
    if not node:
        return False

    for n in g.nodes:
        color = 'gray'
        if n == node:
            color = 'blue'
        elif n in node.neighbors:
            color = 'green'
        plt.plot(n.x, n.y, 'o', color=color)
        plt.text(n.x + 0.1, n.y + 0.1, n.name, fontsize=7)

    for s in g.segments:
        if s.origin == node and s.destination in node.neighbors:
            plt.plot([s.origin.x, s.destination.x], [s.origin.y, s.destination.y], 'r-')
            cx = (s.origin.x + s.destination.x) / 2
            cy = (s.origin.y + s.destination.y) / 2
            plt.text(cx, cy, f"{s.cost:.2f}")
        else:
            plt.plot([s.origin.x, s.destination.x], [s.origin.y, s.destination.y], 'k--', alpha=0.3)
    if g.nodes:
        xs = [n.x for n in g.nodes]
        ys = [n.y for n in g.nodes]
        plt.xlim(min(xs) - 1, max(xs) + 1)
        plt.ylim(min(ys) - 1, max(ys) + 1)

    plt.title(f"Vecinos de {name}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(alpha=0.3)

    return plt.gcf()

def LoadGraphFromFile(filename):
    g = Graph()
    try:
        with open(filename, 'r') as f:
            mode = None
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line == "[Nodes]":
                    mode = "nodes"
                    continue
                elif line == "[Segments]":
                    mode = "segments"
                    continue

                if mode == "nodes":
                    parts = line.split()
                    if len(parts) == 3:
                        name, x, y = parts
                        AddNode(g, Node(name, float(x), float(y)))
                elif mode == "segments":
                    parts = line.split()
                    if len(parts) == 3:
                        name, origin, dest = parts
                        AddSegment(g, name, origin, dest)
    except Exception as e:
        print(f"Error reading file: {e}")
    return g



from path import Path

def FindShortestPath(G, origin_name, dest_name):
    origin = next((n for n in G.nodes if n.name == origin_name), None)
    dest = next((n for n in G.nodes if n.name == dest_name), None)
    if not origin or not dest:
        return None

    current_paths = [Path([origin])]
    while current_paths:
        current_paths.sort(key=lambda p: p.estimated_total_cost(dest))
        path = current_paths.pop(0)
        last = path.last_node()

        if last == dest:
            return path

        for neighbor in last.neighbors:
            if path.contains(neighbor):
                continue
            new_path = path.add_node(neighbor)
            current_paths.append(new_path)
    return None

def GetReachableNodes(G, start_name):
    """
    Retorna una lista de nodos alcanzables desde el nodo inicial.
    """
    start = next((n for n in G.nodes if n.name == start_name), None)
    if not start:
        return []

    visited = set()
    queue = [start]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend([n for n in node.neighbors if n not in visited])

    return list(visited)

def CreateGraph_2():
    G = Graph()

    AddNode(G, Node("X", 1, 1))
    AddNode(G, Node("Y", 4, 1))
    AddNode(G, Node("Z", 2.5, 4))
    AddNode(G, Node("A", 3, 3))
    AddSegment(G, "XY", "X", "Y")
    AddSegment(G, "YZ", "Y", "Z")
    AddSegment(G, "ZA", "Z", "A")
    AddSegment(G, "AX", "A", "X")
    return G