# まずはpythonとして書く。
import random
import numpy as np

__version__ = "0.1"

def find_cycle(neis, Nneis, chain):
    head = chain[-1]
    if len(chain) > 1:
        last = chain[-2]
        nexts = [i for i in neis[head, :Nneis[head]] if i != last]
    else:
        nexts = neis[head, :Nneis[head]]
    # print(nexts)
    while True:
        last=head
        head = random.choice(nexts)
        for i, node in enumerate(chain):
            if node == head:
                return chain[:i], chain[i:]
        chain.append(head)
        nexts = [i for i in neis[head, :Nneis[head]] if i != last]

def remove_cycle(neis, Nneis, cycle):
    for i in range(len(cycle)):
        j = i-1
        if j < 0:
            j += len(cycle)
        a = cycle[i]
        b = cycle[j]
        for k in range(Nneis[a]):
            if neis[a,k] == b:
                neis[a,k] = neis[a,Nneis[a]-1]
                Nneis[a] -= 1
                break
        for k in range(Nneis[b]):
            if neis[b,k] == a:
                neis[b,k] = neis[b,Nneis[b]-1]
                Nneis[b] -= 1
                break


def tileByCycles(neis, Nneis):
    chain = []

    Nedges = np.sum(Nneis)
    while Nedges > 0:
        if len(chain) == 0:
            while True:
                head = random.randint(0, Nneis.shape[0]-1)
                if Nneis[head] > 0:
                    break
            chain = [head]
        chain, cycle = find_cycle(neis, Nneis, chain) # これが遅い。
        yield cycle
        remove_cycle(neis, Nneis, cycle)
        # print(neis)
        # print(Nneis)
        Nedges -= 2*len(cycle)
