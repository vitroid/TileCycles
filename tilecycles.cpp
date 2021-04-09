#include <vector>
#include <iostream>
#include <random>
#include <unistd.h>

using ArrayInt = std::vector< int >;
using ArrayArrayInt = std::vector< ArrayInt >;
using ArrayIntPair = std::pair<ArrayInt, ArrayInt>;

extern std::mt19937 gen;

// random sample one element
int sample(ArrayInt const& a)
{
  return a[gen()%a.size()];
}

ArrayIntPair
find_cycle(ArrayArrayInt const& neis,
           ArrayInt chain)
{
  if ( chain.size() == 0 ){
    int i;
    while (1){
      i = gen() % neis.size();
      if (neis[i].size()>0) break;
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
  for(unsigned int i=0; i<neis[curr].size(); i++){
    if ( neis[curr][i] != prev ){
      nexts.push_back(neis[curr][i]);
    }
  }
  while (1){
    auto next = sample(nexts);
    for(unsigned int i=0; i<chain.size(); i++){
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
    for(unsigned int i=0; i<neis[curr].size(); i++){
      if ( neis[curr][i] != prev ){
        nexts.push_back(neis[curr][i]);
      }
    }
  }
}

void remove_cycle(ArrayArrayInt& neis,
                  ArrayInt const& cycle)
{
  for(unsigned int i=0; i<cycle.size(); i++){
    auto j = i+1;
    if ( j == cycle.size() ){
      j=0;
    }
    auto a = cycle[i];
    auto b = cycle[j];
    for(unsigned int i=0; i<neis[a].size(); i++){
      if (neis[a][i] == b){
        auto tail = neis[a].back();
        neis[a].pop_back();
        if (i != neis[a].size()){
          neis[a][i] = tail;
        }
        break;
      }
    }
    for(unsigned int i=0; i<neis[b].size(); i++){
      if (neis[b][i] == a){
        auto tail = neis[b].back();
        neis[b].pop_back();
        if (i != neis[b].size()){
          neis[b][i] = tail;
        }
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


ArrayArrayInt
tileByCycles(ArrayArrayInt& neis)
{
  ArrayArrayInt cycles;
  ArrayInt chain;

  int nedge = 0;
  for( unsigned int i=0; i< neis.size(); i++){
    nedge += neis[i].size();
  }
  nedge /= 2;

  while ( nedge > 0 ){
    /* disabled. It is available with c++17 and later.
    auto [newchain, cycle] = find_cycle(neis, chain);
    */
    //for c++14
    ArrayIntPair p = find_cycle(neis, chain);
    ArrayInt& newchain = p.first;
    ArrayInt& cycle    = p.second;
    // printArrayInt(cycle, 'o');
    cycles.push_back(cycle);
    chain.assign(newchain.begin(), newchain.end());
    remove_cycle(neis, cycle);
    nedge -= cycle.size();
  }
  return cycles;
}


//動いたっぽい!
//memoryの確保のことを全く考えていないので、これで正しく動いているのか甚だ不安。
//あとはこれにcpythonのインターフェースをつければいい。
//この書き方でいいなら、Fortranを使う必要はないね。
//あとでc++のメモリー構造を勉強する。
