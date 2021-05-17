# The forced depolarization algorithm implemented in Genice.
import numpy as np
import random
import heapq


def shortest_paths(G, start, ends):
    """
    Find all shortests paths from the start to one of the ends.

    Returns:
    list of shortest paths from the start to one of the ends.
    """
    q = [(0, [start, ])]  # Heap of (cost, path)
    visited = set()       # Visited vertices.
    cheapest = 999999
    while len(q):
        # logger.debug(q)
        (cost, path) = heapq.heappop(q)
        if cost > cheapest:
            break
        v0 = path[-1]
        if v0 in ends:
            cheapest = cost  # first arrived
            yield path
        else:
            if v0 in visited:
                continue
            visited.add(v0)
            for v1 in G[v0]:
                if v1 not in visited:
                    heapq.heappush(q, (cost + 1, path + [v1]))


def nearest_to_origin(vertices, coord, cell):
    """
    vertices: a subset of vertices
    coord: fractional coordinates of all vertices
    cell: cell shape
    """
    v = coord[vertices]  # fancy indexing
    v -= np.floor(v + 0.5)
    d = np.sum(v * v, axis=1)
    nearest = np.argmin(d)
    # print(nearest, d[nearest])
    return vertices[nearest]


def net_polarization(dipoles):
    net = 0
    for edge in dipoles:
        net += dipoles[edge]
    return net


def cycle_dipole(cycle, dipoles):
    net = 0
    for i in range(len(cycle)):
        a, b = cycle[i - 1], cycle[i]
        net += dipoles[a, b]
    return net


def invert(cycle, G, dipoles):
    # print(cycle)
    for i in range(len(cycle)):
        a, b = cycle[i - 1], cycle[i]
        dipoles[b, a] = -dipoles[a, b]
        del dipoles[a, b]
        G.remove_edge(a, b)
        G.add_edge(b, a)


def force_depolarize(G, rpos, cell, dipoles):
    net = net_polarization(dipoles)
#     print(net)

    # all vertices.
    # It should be divided into subcells if the system is huge.
    vertices = [x for x in range(rpos.shape[0])]
    for axis in (0, 1, 2):
        unitvec = np.zeros(3)
        unitvec[axis] += 1
        while abs(net[axis]) > 0.1:
            # depolarize in z axis

            # choose a vertex
            center = random.sample(vertices, 1)[0]

            # find the apsis
            apsis = nearest_to_origin(
                vertices, rpos - (rpos[center] + unitvec / 2), cell)
            # for v in (center, apsis):
            #     print(v, rpos[v])

            # find paths and make a directed cycle
            for c2a in shortest_paths(G, center, [apsis]):
                for a2c in shortest_paths(G, apsis, [center]):
                    cycle = c2a[:-1] + a2c[:-1]
                    dip = cycle_dipole(cycle, dipoles)
                    # print(dip)
                    newnet = net - dip * 2
                    if net @ net > newnet @ newnet:
                        # accept and invert.
                        #                         print(f"axis {axis} accepted {len(cycle)}")
                        invert(cycle, G, dipoles)
                        net = newnet
                    break
                break
