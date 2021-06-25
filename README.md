# TileCycles

Tile an even graph with cycles. It is the core part of [GenIce2](https://github.com/vitroid/GenIce) to make a hydrogen-disordered ice structure.


## What is the tiling by cycles?

It is to arrange cycles randomly so that every edge of the graph belongs to one and only one cycle. Such an arrangement of cycles is always possible for an even graph.

## Requirement

* numpy

## API

```python
import tilecycles as tc
cycles = tc.tile(pairs, Nnode)
```
### Inputs
* __pairs__: A 2D numpy array of size m x 2. The values must be numpy.int32. Each value must be in range [0,Nnode) and is the label for a node of the graph.
* __Nnode__: Number of nodes in a graph.

### Output

* __cycles__: A list of numpy arrays of arbitrary size. Each array contains the list of labels constituting a cycle.

## Benchmarks

Run [`TileCycles.ipynb`](https://github.com/vitroid/TileCycles/blob/main/TileCycles.ipynb) on Jupyter or Google Colaboratory.

## Algorithms and how to cite them.

The algorithms to make a depolarized hydrogen-disordered ice are explained in:

M. Matsumoto, T. Yagasaki, and H. Tanaka, "Novel Algorithm to Generate Hydrogen-Disordered Ice Structures.", J. Chem. Info. Modeling, (2021). [DOI:10.1021/acs.jcim.1c00440](https://doi.org/10.1021/acs.jcim.1c00440)

    @article{Matsumoto:2021,
        author = {Matsumoto, Masakazu and Yagasaki, Takuma and Tanaka, Hideki},
        title = {Novel Algorithm to Generate Hydrogen-Disordered Ice Structures},
        journal = {Journal of Chemical Information and Modeling},
        volume = {},
        pages = {},
        year = {2021}
    }

## Note

I rewrote the algorithm in C++, which is available as the `tilecycles_c` module. However, I decided to unuse it in GenIce2 2.1 because the contribution to the improvement in speed is found to be only a little. Python version is fast enough for the purpose.
