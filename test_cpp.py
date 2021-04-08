import numpy as np
#from f_tilecycles import find_cycle, remove_cycle
import random

import c_tilecycles as tc # pyx

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

# make the pair list
pairs = []
for i,j in raw["graph"].edges():
    pairs.append([i,j])
pairs = np.array(pairs, dtype=np.int32)
Nnode = raw['reppositions'].shape[0]

now = time.time()
cycles = tc.tile(pairs, Nnode)
print(time.time() - now)
