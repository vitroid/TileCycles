#include "tilecycles.hpp"

int main(int argc, char *argv[])
{
  ArrayInt neis{1,2,3,4,
                   0,2,3,5,
                   0,1,4,5,
                   0,1,4,5,
                   0,2,3,5,
                   1,2,3,4};

  ArrayInt Nneis{4,4,4,4,4,4};

  ArrayArrayInt cycles = tileByCycles(neis, Nneis);

  for(auto it = cycles.begin(); it != cycles.end(); ++it){
    auto cycle = *it;
    printArrayInt(cycle, 'c');
  }
}

