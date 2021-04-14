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
raw = GenIce(lattice, rep=(3,3,3)).generate_ice(water, formatter)

pairs = []
for i,j in raw["graph"].edges():
    pairs.append([i,j])
pairs = np.array(pairs, dtype=np.int32)
Nnode = raw['reppositions'].shape[0]

now = time.time()
seed = 1111
cycles = ctc.tile(pairs, Nnode, seed)
print(time.time() - now, "c++")
print(cycles[0])

now = time.time()
cycles = tc.tile(pairs, Nnode)
print(time.time() - now, "python")
print(cycles[0])

dip = tc.dipoles(cycles, raw['reppositions'])
print(dip)


# 2021-04-05現状報告
# tcはgenice2より少し速い。ただし、genice2のStage3Dのすべてを実装しているわけではないので、たぶん実質的には同じ速度なんだろう。
# tcxはそれに比べて4倍ぐらい速い。たしかに速いが、桁違いというほどでもない。
# 完全にCで実装して、10倍速くなるなら試してもいいかも。
# だいたい書き方はわかってきた。
