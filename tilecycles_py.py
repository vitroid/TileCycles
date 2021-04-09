# まずはpythonとして書く。
import random
import numpy as np
from collections import defaultdict

__version__ = "0.1.1"

def find_cycle(neis, chain):
    head = chain[-1]
    if len(chain) > 1:
        last = chain[-2]
        nexts = [i for i in neis[head] if i != last]
    else:
        nexts = neis[head]
    # print(nexts)
    while True:
        last=head
        head = random.choice(nexts)
        for i, node in enumerate(chain):
            if node == head:
                return chain[:i], chain[i:]
        chain.append(head)
        nexts = [i for i in neis[head] if i != last]

def remove_cycle(neis, cycle):
    for i in range(len(cycle)):
        j = i-1
        if j < 0:
            j += len(cycle)
        a = cycle[i]
        b = cycle[j]
        neis[a].remove(b)
        neis[b].remove(a)
        if len(neis[a]) == 0:
            del neis[a]
        if len(neis[b]) == 0:
            del neis[b]


def tileByCycles(neis):
    chain = []
    while len(neis) > 0:
        if len(chain) == 0:
            head = random.choice(list(neis))
            chain = [head]
        chain, cycle = find_cycle(neis, chain)
        yield cycle
        remove_cycle(neis, cycle)

def tile(pairs, Nnode):
    neis = defaultdict(list)
    for i,j in pairs:
        neis[i].append(j)
        neis[j].append(i)
    return [cycle for cycle in tileByCycles(neis)]
