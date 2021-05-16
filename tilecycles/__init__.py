import random
import numpy as np
import networkx as nx
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
            return chain[:i+1], chain[i:]
        # otherwise, mark the new head position
        order[head] = len(chain)
        chain.append(head)


def remove_cycle(g, cycle, order):
    # unmark vertices in the cycle (except for the first vertecx)
    for i in range(1, len(cycle)):
        order[cycle[i]] = -1
    # remove edges of the cycle
    for i in range(len(cycle)):
        a = cycle[i-1]
        b = cycle[i]
        g.remove_edge(a, b)
    # remove edgeless vertices in the graph
    for a in cycle:
        if g.degree(a) == 0:
            g.remove_node(a)


def tileByCycles(g, Nnode=-1):
    # random walk path
    chain = []
    # markers that indicate the orders in the path
    if Nnode < 0:
        Nnode = g.number_of_nodes()
    order = -np.ones(Nnode, dtype=np.int)
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


def tile(pairs, Nnode=-1, seed=-1):
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
        r = random.randint(0, Ncycle-1)
        newnet = net - 2*direction[r]*cycdip[r]
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
    for i in range(len(path)-1):
        G.remove_edge(path[i], path[i+1])
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
