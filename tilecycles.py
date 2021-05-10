# まずはpythonとして書く。
import random
from collections import defaultdict


def find_cycle(neis, chain, order):
    head = chain[-1]
    if len(chain) > 1:
        last = chain[-2]
        nexts = [i for i in neis[head] if i != last]
    else:
        nexts = neis[head]
    # print(nexts)
    while True:
        last = head
        head = random.choice(nexts)
        i = order[head]
        if i == 0:
            order[head] = -1
            return [], chain
        elif i > 0:
            return chain[:i + 1], chain[i:]
        order[head] = len(chain)
        chain.append(head)
        nexts = [i for i in neis[head] if i != last]


def remove_cycle(neis, cycle, order):
    for i in range(1, len(cycle)):
        order[cycle[i]] = -1
    for i in range(len(cycle)):
        a = cycle[i]
        b = cycle[i - 1]
        neis[a].remove(b)
        neis[b].remove(a)
    for node in cycle:
        if len(neis[node]) == 0:
            del neis[node]


def tileByCycles(neis):
    chain = []
    order = [-1] * len(neis)
    while len(neis) > 0:
        if len(chain) == 0:
            head = random.choice(list(neis))
            chain = [head]
            order[head] = 0
        chain, cycle = find_cycle(neis, chain, order)
        yield cycle
        remove_cycle(neis, cycle, order)


def tile(pairs, Nnode):
    neis = defaultdict(list)
    for i, j in pairs:
        neis[i].append(j)
        neis[j].append(i)
    return [cycle for cycle in tileByCycles(neis)]
