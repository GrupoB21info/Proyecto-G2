from graph import *

def CreateGraph_1():
    G = Graph()
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddSegment(G, "AB","A","B")
    AddSegment(G, "AE","A","E")
    AddSegment(G, "AK","A","K")
    AddSegment(G, "BA","B","A")
    AddSegment(G, "BC","B","C")
    AddSegment(G, "BF","B","F")
    AddSegment(G, "BK","B","K")
    AddSegment(G, "BG","B","G")
    AddSegment(G, "CD","C","D")
    AddSegment(G, "CG","C","G")
    AddSegment(G, "DG","D","G")
    AddSegment(G, "DH","D","H")
    AddSegment(G, "DI","D","I")
    AddSegment(G, "EF","E","F")
    AddSegment(G, "FL","F","L")
    AddSegment(G, "GB","G","B")
    AddSegment(G, "GF","G","F")
    AddSegment(G, "GH","G","H")
    AddSegment(G, "ID","I","D")
    AddSegment(G, "IJ","I","J")
    AddSegment(G, "JI","J","I")
    AddSegment(G, "KA","K","A")
    AddSegment(G, "KL","K","L")
    AddSegment(G, "LK","L","K")
    AddSegment(G, "LF","L","F")
    return G

G = CreateGraph_1()
Plot(G)
PlotNode(G, "C")
n = GetClosest(G,15,5)
print(n.name)  # J
n = GetClosest(G,8,19)
print(n.name)  # B
# Prueba de carga desde archivo
print("\nProbando carga desde archivo...")
filename = "grafo_test.txt"

with open(filename, "w") as f:
    f.write("""[Nodes]
A 1 0
B 4 0
C 2 3
D 2 8
E 1 8
F 3 7
G 4 4
H 1 3
[Segments]
S1 A B
S2 B C
S3 C D
S4 D E
S5 E F
S6 F G
S7 G H
S8 H A
""")

G2 = LoadGraphFromFile(filename)
Plot(G2)
PlotNode(G2, "A")
print("Nodo más cercano a (1,1):", GetClosest(G2, 1, 1).name)