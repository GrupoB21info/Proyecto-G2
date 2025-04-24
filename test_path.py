from graph import CreateGraph_1
from path import *

G = CreateGraph_1()
A = next(n for n in G.nodes if n.name == "A")
K = next(n for n in G.nodes if n.name == "K")
L = next(n for n in G.nodes if n.name == "L")

p1 = Path([A, K])
print("Coste real:", p1.real_cost)

p2 = p1.add_node(L)
print("Nuevo camino:", [n.name for n in p2.nodes])
print("Coste estimado hasta F:", p2.estimated_total_cost(next(n for n in G.nodes if n.name == "F")))
