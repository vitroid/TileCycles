import random


def six(d, Nnode, MaxSize=1e99):
    """
    find a cyclic path in the given digraph.
    d: digraph (networkx.DiGraph)
    """
    head = random.randint(0, Nnode - 1)
    path = [head]
    while True:
        nexts = list(d.successors(head))
        next = random.choice(nexts)
        if next in path:
            i = path.index(next)
            if len(path[i:]) >= MaxSize:
                # print("Drop.")
                return []
            return path[i:]
        path.append(next)
        head = next


def invertCycle(d, cycle, g_footprint):
    for i in range(len(cycle)):
        a, b = cycle[i - 1], cycle[i]
        d.remove_edge(a, b)
        d.add_edge(b, a)
        # footprint
        if g_footprint.has_edge(a, b):
            g_footprint.remove_edge(a, b)
