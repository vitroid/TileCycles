#include <vector>
#include <iostream>
#include <random>
#include <unistd.h>

using ArrayInt = std::vector< int >;
std::mt19937 gen(getpid());

int sample(ArrayInt const& a)
{
  return a[gen()%a.size()];
}

std::pair<ArrayInt, ArrayInt>
find_cycle(ArrayInt const& nei,
           ArrayInt const& Nnei,
           ArrayInt chain)
{
  if ( chain.size() == 0 ){
    int i;
    while (1){
      i = gen() % Nnei.size();
      if (Nnei[i]>0) break; 
    }
    chain.push_back(i);
  }
  auto chain_size = chain.size();
  auto curr = chain[chain_size-1];
  ArrayInt nexts;
  auto prev = -1;
  if (chain_size > 1){
    prev = chain[chain_size-2];
  }
  for(int i=0; i<Nnei[curr]; i++){
    if ( nei[curr*4+i] != prev ){
      nexts.push_back(nei[curr*4+i]);
    }
  }
  while (1){
    auto next = sample(nexts);
    for(int i=0; i<chain.size(); i++){
      if (chain[i] == next){
        ArrayInt cycle(chain.size() - i);
        auto start = chain.begin() + i;
        auto end = chain.end();
        copy(start, end, cycle.begin());
        chain.resize(i);
        return std::make_pair(chain, cycle);
      }
    }
    chain.push_back(next);
    prev = curr;
    curr = next;
    nexts.resize(0);
    for(int i=0; i<Nnei[curr]; i++){
      if ( nei[curr*4+i] != prev ){
        nexts.push_back(nei[curr*4+i]);
      }
    }
  }
}

void remove_cycle(ArrayInt& neis,
                  ArrayInt& Nneis,
                  ArrayInt const& cycle)
{
  for(auto i=0; i<cycle.size(); i++){
    auto j = i+1;
    if ( j == cycle.size() ){
      j=0;
    }
    auto a = cycle[i];
    auto b = cycle[j];
    for(auto i=0; i<Nneis[a]; i++){
      if (neis[a*4+i] == b){
        Nneis[a] --;
        neis[a*4+i] = neis[a*4+Nneis[a]];
        break;
      }
    }
    for(auto i=0; i<Nneis[b]; i++){
      if (neis[b*4+i] == a){
        Nneis[b] --;
        neis[b*4+i] = neis[b*4+Nneis[b]];
        break;
      }
    }
  }
}


void
printArrayInt(ArrayInt const& a, char c)
{
  std::cout << c;
  for ( auto it = a.begin(); it != a.end(); ++it )
      std::cout << ' ' << *it;
  std::cout << "\n";
}

using ArrayArrayInt = std::vector< ArrayInt >;

ArrayArrayInt
tileByCycles(ArrayInt& neis, ArrayInt& Nneis)
{
  ArrayArrayInt cycles;
  ArrayInt chain;

  int nedge = Nneis.size() * 2; // assume a normal ice.

  while ( nedge > 0 ){
    auto [newchain, cycle] = find_cycle(neis, Nneis, chain);
    printArrayInt(cycle, 'o');
    cycles.push_back(cycle);
    chain.assign(newchain.begin(), newchain.end());
    remove_cycle(neis, Nneis, cycle);
    nedge -= cycle.size();
  }
  return cycles;
}


//動いたっぽい!
//memoryの確保のことを全く考えていないので、これで正しく動いているのか甚だ不安。
//あとはこれにcpythonのインターフェースをつければいい。
//この書き方でいいなら、Fortranを使う必要はないね。
//あとでc++のメモリー構造を勉強する。


