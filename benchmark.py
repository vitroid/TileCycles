import numpy as np
#from f_tilecycles import find_cycle, remove_cycle
import random

import tilecycles_py as tc
import tilecycles as ctc

import time

# まずは部品単位で高速化

# 辞書と集合を使わないようにするために、グラフをこういう隣接行列で表現する。
# neis = np.array([[1,2,3,4],
#                  [0,2,3,5],
#                  [0,1,4,5],
#                  [0,1,4,5],
#                  [0,2,3,5],
#                  [1,2,3,4]], dtype=np.int32)
# Nneis = np.array([4]*6, dtype=np.int32)


from genice2.genice import GenIce
from genice2.plugin import Lattice, Format, Molecule

lattice    = Lattice("1c")
formatter  = Format("raw", stage=(1,2,))
water      = Molecule("spce")
raw = GenIce(lattice, rep=(20,20,20)).generate_ice(water, formatter)

pairs = []
for i,j in raw["graph"].edges():
    pairs.append([i,j])
pairs = np.array(pairs, dtype=np.int32)
Nnode = raw['reppositions'].shape[0]

now = time.time()
seed = 1112
cycles = ctc.tile(pairs, Nnode, seed)
print(time.time() - now, "c++")
print(cycles[0])

random.seed(seed)
now = time.time()
cycles = tc.tile(pairs, Nnode)
print(time.time() - now, "python")
print(cycles[0])






def _dipole(cycle, ipos):
    """
    Returns the sum of the vectors that make up the cycle.

    ipos are the relative positions in the periodic boundary parallelepiped cell, and are integers between 0 and 65535.
    If the cycle does not cross the cell boundary, it is (0,0,0), and if it crosses in the x direction, it is (±65536,0,0).
    """
    d = ipos[cycle] - ipos[np.roll(cycle, 1)]
    d = (d+32768) % 65536 - 32768
    # print(d)
    return np.sum(d, axis=0) // 65536


def dipoles(cycles, relpos):
    ipos = (relpos * 65536).astype(int)
    d = np.zeros([len(cycles), 3], dtype=np.int)
    for i, cycle in enumerate(cycles):
        d[i] = _dipole(cycle, ipos)
    return d


# Depolarize

dip = dipoles(cycles, raw['reppositions'])
ind = []            # indices of non-zero dipole
parity = dict()     # +/- 1
vec = np.zeros(3)   # net dipole
for i, d in enumerate(dip):
    if d@d > 0:
        ind.append(i)
        parity[i] = 1
        vec += d
sca = vec@vec
print(vec)
while sca > 0:
    # select one cycle
    i = random.choice(list(parity.keys()))

    # invert it
    newvec = vec - dip[i]*2*parity[i]

    # if the inversion reduces the net dipole
    if newvec@newvec <= sca:
        print(newvec)
        # accept inversion
        vec = newvec
        sca = vec@vec
        parity[i] = -parity[i]
# verify final net dipole
vec = np.zeros(3)
for i, d in enumerate(dip):
    if d@d > 0:
        vec += d*parity[i]
print(vec)



# 2021-04-05現状報告
# tcはgenice2より少し速い。ただし、genice2のStage3Dのすべてを実装しているわけではないので、たぶん実質的には同じ速度なんだろう。
# tcxはそれに比べて4倍ぐらい速い。たしかに速いが、桁違いというほどでもない。
# 完全にCで実装して、10倍速くなるなら試してもいいかも。
# だいたい書き方はわかってきた。
