import random

import networkx as nx
import numpy as np

import tilecycles.Dipole as dp


def find_cycle(g, chain, order):
    # head of the snake
    head = chain[-1]
    # neck is the vertex next to head
    neck = -1
    if len(chain) > 1:
        neck = chain[-2]
    while True:
        # candidates for the next step
        candids = [i for i in g[head] if i != neck]
        # go ahead
        neck = head
        head = random.choice(candids)
        # lookup the new head in the markers
        i = order[head]
        # if it is marked as the tail end of the snake,
        if i == 0:
            # the random walk returns to the first node of the chain;
            # unmark the head.
            order[head] = -1
            # return an empty chain and a cycle
            return [], chain
        # if the random walk crosses at an intermediate node of the chain,
        elif i > 0:
            # return a chain and a cycle
            return chain[:i + 1], chain[i:]
        # otherwise, mark the new head position
        order[head] = len(chain)
        chain.append(head)


def remove_cycle(g, cycle, order):
    # unmark vertices in the cycle (except for the first vertex)
    for i in range(1, len(cycle)):
        order[cycle[i]] = -1
    # remove edges of the cycle
    for i in range(len(cycle)):
        a = cycle[i - 1]
        b = cycle[i]
        g.remove_edge(a, b)
    # remove edgeless vertices in the graph
    for a in cycle:
        if g.degree(a) == 0:
            g.remove_node(a)


def tileByCycles(g):
    # random walk path
    chain = []
    Nnode = g.number_of_nodes()
    # markers that indicate the orders in the path
    order = -np.ones(Nnode, dtype=int)
    while g.number_of_nodes() > 0:
        # if the chain is empty
        if len(chain) == 0:
            # randomly select the "head" node.
            head = random.choice(list(g.nodes()))
            chain = [head]
            # mark it as the first node.
            order[head] = 0
        # walk randomly to find a cycle.
        chain, cycle = find_cycle(g, chain, order)
        # found.
        yield cycle
        # remove it from the graph and unmark.
        remove_cycle(g, cycle, order)


def tileByCycles2(g):
    """
    Trial for more homogeneous sampling by node division.
    According to the idea by Prof. Sakuma at Akita University.
    However, it results in very huge cycles, that are not suitable for depolarization.
    Also, it is a little bit slower than tileByCycles().
    """
    def labels(nodes):
        newn = []
        for node in nodes:
            if node < 0:
                newn.append(-1-node)
            else:
                newn.append(node)
        return newn

    # Double the nodes
    # Give negative numbers for the duplicated nodes
    Nnode = g.number_of_nodes()
    for i in range(Nnode):
        doppel = -i-1
        assert not g.has_node(doppel)
        g.add_node(doppel)
        nei = [j for j in g.neighbors(i)]
        assert len(nei) == 4, g[i]
        for v in random.sample(nei, 2):
            g.remove_edge(i, v)
            g.add_edge(doppel, v)
    while g.number_of_nodes() > 0:
        cycle = []
        head = list(g.nodes())[0]
        nei = [j for j in g.neighbors(head)]
        # print(nei)
        cycle.append(head)
        last = head
        succ = random.choice(nei)
        # print(succ)
        while succ != head:
            cycle.append(succ)
            # print(cycle)
            nei = [j for j in g.neighbors(succ)]
            assert len(nei) == 2
            s2 = nei[0]
            if s2 == last:
                s2 = nei[1]
            last, succ = succ, s2
        yield labels(cycle)
        for v in cycle:
            g.remove_node(v)



def tile(pairs):
    """
    Nnode and seed are dummpy parameters
    for the compatibility with c++ codes.
    """
    g = nx.Graph()
    g.add_edges_from(pairs)
    return [cycle for cycle in tileByCycles(g)]


def depolarize(cycles, dipoles, dd, rpos, cell):
    # pick up the traversing cycles
    cid = []
    cycdip = []
    direction = []
    for i, cycle in enumerate(cycles):
        dip = dp.cycle_dipole(cycle, dipoles)
        if not np.allclose(dip, 0):
            cid.append(i)
            cycdip.append(dip)
            direction.append(1)
    cycdip = np.array(cycdip)
    direction = np.array(direction)
    Ncycle = cycdip.shape[0]

    # reduce polarization by flipping cycles randomly
    net = dp.net_polarization(dipoles)
    count = 100
    while not np.allclose(net, 0):
        r = random.randint(0, Ncycle - 1)
        newnet = net - 2 * direction[r] * cycdip[r]
        if net @ net > newnet @ newnet:
            direction[r] = -direction[r]
            net = newnet
        count -= 1
        if count == 0:
            print("give up depolarizing completely.")
            break

    # reflect the inversions to the dipoles and graph
    for i in range(Ncycle):
        if direction[i] < 0:
            dp.invert(cycles[cid[i]], dd, dipoles)

    if not np.allclose(net, 0):
        print("Original GenIce algorithm.")
        dp.force_depolarize(dd, rpos, cell, dipoles)
        return 1
    else:
        return 0


# For odd-odd chains
def remove_path(G, path):
    for i in range(len(path) - 1):
        G.remove_edge(path[i], path[i + 1])
    for node in path:
        if len(G[node]) == 0:
            G.remove_node(node)


def odd_chains(g):
    # make a list of odd vertices
    odds = set([node for node in g if len(g[node]) % 2 == 1])

    # couple them.
    while len(odds) > 0:
        node = odds.pop()
        for path in dp.shortest_paths(g, node, odds):
            end = path[-1]
            assert end in odds
            odds.remove(end)
            yield path
            break
