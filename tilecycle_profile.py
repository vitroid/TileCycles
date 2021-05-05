import cProfile
from genice2.genice import GenIce
from genice2.plugin import Lattice, Format, Molecule

import networkx as nx
import numpy as np
import random
import time


from collections import defaultdict


def test_icerule(d, N):
    assert d.number_of_nodes() == N
    for node in d:
        assert d.in_degree(node) == 2
        assert d.in_degree(node) == 2


def find_cycle(g, chain):
    head = chain[-1]
    last = -1
    if len(chain) > 1:
        last = chain[-2]
    while True:
        nexts = [i for i in g[head] if i != last]
        last = head
        head = random.choice(nexts)
        if head in chain:
            i = chain.index(head)
            return chain[:i], chain[i:]
        chain.append(head)


def remove_cycle(g, cycle):
    for i in range(len(cycle)):
        a = cycle[i - 1]
        b = cycle[i]
        g.remove_edge(a, b)
    for a in cycle:
        if g.degree(a) == 0:
            g.remove_node(a)


def tileByCycles(g):
    chain = []
    while g.number_of_nodes() > 0:
        if len(chain) == 0:
            head = random.choice(list(g.nodes()))
            chain = [head]
        chain, cycle = find_cycle(g, chain)
        yield cycle
        remove_cycle(g, cycle)


def core(g):
    dd = nx.DiGraph()
    for cycle in tileByCycles(g):
        if random.randint(0, 1) == 0:
            nx.add_cycle(dd, cycle)
        else:
            nx.add_cycle(dd, cycle[::-1])
    return dd


def main():

    lattice = Lattice("1c")
    formatter = Format("raw", stage=(2,))  # generates an undirected graph
    water = Molecule("spce")

    gen = []
    N = 40
    raw = GenIce(lattice, rep=[N, N, N]).generate_ice(water, formatter)
    g0 = raw['graph']
    Nnode = g0.number_of_nodes()

    # 一旦無向グラフになおし、

    g = nx.Graph(g0)
    dd = core(g)
    test_icerule(dd, Nnode)


cProfile.run("main()")
