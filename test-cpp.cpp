#include "tilecycles.hpp"

int main(int argc, char *argv[])
{
  ArrayArrayInt neis{{1,2,3,4},
                     {0,2,3,5},
                     {0,1,4,5},
                     {0,1,4,5},
                     {0,2,3,5},
                     {1,2,3,4}};

  ArrayArrayInt cycles = tileByCycles(neis);

  for(auto it = cycles.begin(); it != cycles.end(); ++it){
    auto cycle = *it;
    printArrayInt(cycle, 'c');
  }
}



//pythonと連携させる時には、ペアリストを渡すのが一番単純で良い。
//整数の1次元配列ですむ。
//インターフェースは実はf2pyにやらせるのがいいのでは?
