from node import Distance

class Path:
    def __init__(self, nodes):
        self.nodes = nodes  # Lista de nodos
        self.real_cost = self.calculate_real_cost()

    def calculate_real_cost(self):
        if len(self.nodes) < 2:
            return 0
        return sum(Distance(self.nodes[i], self.nodes[i+1]) for i in range(len(self.nodes) - 1))

    def estimated_total_cost(self, destination):
        return self.real_cost + Distance(self.nodes[-1], destination)

    def last_node(self):
        return self.nodes[-1]

    def contains(self, node):
        return node in self.nodes

    def add_node(self, node):
        return Path(self.nodes + [node])

def PlotPath(graph, path):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14, 10))
    plt.clf()

    for node in graph.nodes:
        plt.plot(node.x, node.y, 'o', color='gray')
        plt.text(node.x + 0.1, node.y + 0.1, node.name, fontsize=7)


    for seg in graph.segments:
        plt.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'k--', alpha=0.3)

    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i+1]
        plt.plot([n1.x, n2.x], [n1.y, n2.y], 'r-', linewidth=2)


    if graph.nodes:
        xs = [n.x for n in graph.nodes]
        ys = [n.y for n in graph.nodes]
        plt.xlim(min(xs) - 1, max(xs) + 1)
        plt.ylim(min(ys) - 1, max(ys) + 1)

    plt.title("Camino más corto")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(alpha=0.3)

    return plt.gcf()
