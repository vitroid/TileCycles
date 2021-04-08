import numpy as np
#from f_tilecycles import find_cycle, remove_cycle
import random

import pyximport
# pyximport.install(setup_args={"include_dirs":np.get_include()},
#                   reload_support=True)
pyximport.install()
import tilecycles_cython as tcx # pyx
import tilecycles as tc
import c_tilecycles as ctc # pyx

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
raw = GenIce(lattice, rep=(30,30,30)).generate_ice(water, formatter)

neis  = np.zeros((raw['reppositions'].shape[0],4), dtype=np.int32)
Nneis = np.zeros(raw['reppositions'].shape[0], dtype=np.int32)

for i,j in raw['graph'].edges():
    neis[i, Nneis[i]] = j
    Nneis[i] += 1
    neis[j, Nneis[j]] = i
    Nneis[j] += 1

now = time.time()
for cycle in tc.tileByCycles(neis, Nneis):
    pass #print(cycle)
print(time.time() - now, "python")

neis  = np.zeros((raw['reppositions'].shape[0],4), dtype=np.int32)
Nneis = np.zeros(raw['reppositions'].shape[0], dtype=np.int32)

for i,j in raw['graph'].edges():
    neis[i, Nneis[i]] = j
    Nneis[i] += 1
    neis[j, Nneis[j]] = i
    Nneis[j] += 1

now = time.time()
for cycle in tcx.tileByCycles(neis, Nneis):
    pass #print(cycle)
print(time.time() - now, "cython")

pairs = []
for i,j in raw["graph"].edges():
    pairs.append([i,j])
pairs = np.array(pairs, dtype=np.int32)
Nnode = raw['reppositions'].shape[0]

now = time.time()
cycles = ctc.tile(pairs, Nnode)
print(time.time() - now, "c++")



# 2021-04-05現状報告
# tcはgenice2より少し速い。ただし、genice2のStage3Dのすべてを実装しているわけではないので、たぶん実質的には同じ速度なんだろう。
# tcxはそれに比べて4倍ぐらい速い。たしかに速いが、桁違いというほどでもない。
# 完全にCで実装して、10倍速くなるなら試してもいいかも。
# だいたい書き方はわかってきた。
