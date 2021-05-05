import numpy as np
#from f_tilecycles import find_cycle, remove_cycle


neis = np.array([[1, 2, 3, 4],
                 [0, 2, 3, 5],
                 [0, 1, 4, 5],
                 [0, 1, 4, 5],
                 [0, 2, 3, 5],
                 [1, 2, 3, 4]], dtype=np.int32)
Nneis = np.array([4] * 6, dtype=np.int32)

chain = [0, 1]

# f2py
# neis = np.array([[2,3,4,5],
#                   [1,3,4,6],
#                   [1,2,5,6],
#                   [1,2,5,6],
#                   [1,3,4,6],
#                   [2,3,4,5]], dtype=np.int32)
# Nneis = np.array([4]*6, dtype=np.int32)
#
# chain = np.zeros(6, dtype=np.int32)
# chain[:2] = [1,2]
# Nchain = 2
#
# cycle = np.zeros(6, dtype=np.int32)
# Ncycle, Newchain = find_cycle(neis, Nneis, chain, Nchain, cycle )
# python
chain, cycle = find_cycle(neis, Nneis, chain)
print(cycle, "cycle")
print(chain, "chain")
print(neis, Nneis)
# f2py
# print(cycle, Ncycle, "cycle")
# print(chain, Newchain, "chain")
# print(neis, Nneis)
# print(neis.flags.c_contiguous)
# print(neis.flags.f_contiguous)
# neis = np.asfortranarray(neis)
# Nneis = np.asfortranarray(Nneis)
# remove_cycle(neis,Nneis, cycle, Ncycle)
# python
remove_cycle(neis, Nneis, cycle)
print(neis, Nneis)

# いろいろふわふわしてて気にいらないね。
# やはりC++で書くことになるのか。

# 訳のわからないしがらみ(配列が1からはじまるとか、メモリーの並び順が違うとか、assumed配列の長さがうまくわたらないとか)を考えながらfortranで書くよりは、fortran的な書き方でcythonで書いたほうが、読めるコードが書ける気がする。そうしよう。
