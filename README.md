# TileCycles

Tile an even graph with cycles. It is the core part of GenIce2 to make a hydrogen-disordered ice structure.


## What is the tiling by cycles?

It is to arrange cycles randomly so that every edge of the graph belongs to one and only one cycle. Such an arrangement of cycles is always possible for an even graph.

## Requirement

* numpy

## API

```python
import tilecycles as tc
cycles = tc.tile(pairs, Nnode, seed)
```
### Inputs
* __pairs__: A 2D numpy array of size m x 2. The values must be numpy.int32. Each value must be in range [0,Nnode) and is the label for a node of the graph.
* __Nnode__: Number of nodes in a graph.
* __seed__: Random seed.

### Output
* __cycles__: A list of numpy arrays of arbitrary size. Each array contains the list of labels constituting a cycle.

## ToDos

* Depolarizer should be implemented.

## Benchmarks
Run `TileCycles.ipynb` on Jupyter for finer benchmarkings.

Ic, 30x30x30, tiling only, on Apple M1 using the `benchmark.py`.
```shell
% python benchmark.py
0.09434318542480469 c++
1.2123610973358154 python
```

Ic, 40x40x40, tiling only, on Apple M1 using the `benchmark.py`.
```shell
% python benchmark.py
0.26435399055480957 c++
3.587411880493164 python
```
