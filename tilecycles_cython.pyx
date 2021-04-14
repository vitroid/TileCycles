# まずはpythonとして書く。
import random
import numpy as np
# cimport numpy as np
DTYPE = np.int32
# cdef extern double genrand64_real2()

import pymt64
# cimport PyMT64

mt = pymt64.init(111)

def choice(L):
    # cdef int i = int(genrand64_real2()*len(L))
    cdef int i = int(pymt64.uniform(mt,1)[0]*len(L))
    return L[i]

# def find_cycle(np.ndarray neis, np.ndarray Nneis, chain):
def find_cycle(neis, Nneis, chain):
    cdef int head, last, node, i
    assert neis.dtype == DTYPE
    assert Nneis.dtype == DTYPE
    # assert chain.dtype == DTYPE
    head = chain[-1]
    if len(chain) > 1:
        last = chain[-2]
        nexts = [i for i in neis[head, :Nneis[head]] if i != last]
    else:
        nexts = neis[head, :Nneis[head]]
    # print(nexts)
    while True:
        last = head
        # head = random.choice(nexts)
        head = choice(nexts)
        for i, node in enumerate(chain):
            if node == head:
                return chain[:i], chain[i:]
        chain.append(head)
        nexts = [i for i in neis[head, :Nneis[head]] if i != last]

# def remove_cycle(np.ndarray neis, np.ndarray Nneis, cycle):
def remove_cycle(neis, Nneis, cycle):
    cdef int i,j,k,a,b, Ncycle
    assert neis.dtype == DTYPE
    assert Nneis.dtype == DTYPE
    Ncycle = len(cycle)
    # assert cycle.dtype == DTYPE
    for i in range(Ncycle):
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


def tile(pairs, Nnode):
    neis  = np.zeros((Nnode,4), dtype=np.int32)
    Nneis = np.zeros(Nnode, dtype=np.int32)
    for i,j in pairs:
        neis[i, Nneis[i]] = j
        Nneis[i] += 1
        neis[j, Nneis[j]] = i
        Nneis[j] += 1

    return [cycle for cycle in tileByCycles(neis, Nneis)]
