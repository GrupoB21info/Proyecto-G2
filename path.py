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
    fig, ax = plt.subplots()
    for node in graph.nodes:
        ax.plot(node.x, node.y, 'o', color='gray')
        ax.text(node.x, node.y, node.name)

    for seg in graph.segments:
        ax.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'k--', alpha=0.3)

    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i+1]
        ax.plot([n1.x, n2.x], [n1.y, n2.y], 'r-', linewidth=2)

    ax.set_title("Camino más corto")
    return fig