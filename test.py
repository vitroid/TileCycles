from genice2.genice import GenIce
from genice2.plugin import Lattice, Format, Molecule
from tilecycles import tileByCycles, tileByCycles2
import networkx as nx
import time

lattice = Lattice("1c")
formatter = Format("raw", stage=(1,2,))  # generates an undirected graph

N = 16
raw = GenIce(lattice, rep=[N, N, N]).generate_ice(formatter)
g0 = nx.Graph(raw['graph'])
Nnode = g0.number_of_nodes()

N = 0
now = time.time()
for cycle in tileByCycles2(g0):
    N += len(cycle)
delta = time.time() - now
print(N, Nnode, delta)

g0 = nx.Graph(raw['graph'])
N = 0
now = time.time()
for cycle in tileByCycles(g0):
    N += len(cycle)
delta = time.time() - now
print(N, Nnode, delta)