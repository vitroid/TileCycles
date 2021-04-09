# TileCycles

Tile an even graph with cycles. It is the core part of GenIce2 to make a hydrogen-disordered ice structure.

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
Ic, 30x30x30, tiling only, on Apple M1.
```shell
% python benchmark.py
18.11472511291504 python
4.384294033050537 cython
0.3890860080718994 c++
```
