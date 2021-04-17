#include <vector>
#include <iostream>
#include <random>
#include <unistd.h>

using ArrayInt = std::vector< int >;
using ArrayArrayInt = std::vector< ArrayInt >;
using ArrayIntPair = std::pair<ArrayInt, ArrayInt>;

extern std::mt19937 gen;
void
printArrayInt(ArrayInt const& a, char c);

// random sample one element
int sample(ArrayInt const& a)
{
  return a[gen()%a.size()];
}

ArrayIntPair
find_cycle(ArrayArrayInt const& neis,
           ArrayInt  chain,
           ArrayInt& order)
{
  if ( chain.size() == 0 ){
    int i;
    while (1){
      i = gen() % neis.size();
      if (neis[i].size()>0) break;
    }
    chain.push_back(i);
    order[i] = 0;
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
    auto i    = order[next];
    if ( i == 0 ){
      ArrayInt empty(0);
      order[chain[0]] = -1;
      return std::make_pair(empty, chain);
    }
    else if (i > 0){
      ArrayInt cycle(chain.size() - i);
      auto start = chain.begin() + i;
      auto end = chain.end();
      copy(start, end, cycle.begin());
      chain.resize(i+1);
      return std::make_pair(chain, cycle);
    }
    order[next] = chain.size();
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


void remove_neighbor(ArrayArrayInt& neis,
                 int a,
                 int b)
{
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
}

void remove_cycle(ArrayArrayInt& neis,
                  ArrayInt const& cycle,
                  ArrayInt&       order)
{
  size_t L = cycle.size();
  for(unsigned int i=1; i<L; i++){
    order[cycle[i]] = -1;
  }
  for(unsigned int i=0; i<L; i++){
    auto j = i+1;
    if ( j == L ){
      j=0;
    }
    auto a = cycle[i];
    auto b = cycle[j];
    remove_neighbor(neis, a, b);
    remove_neighbor(neis, b, a);
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
  ArrayInt order(neis.size());

  int nedge = 0;
  for( unsigned int i=0; i< neis.size(); i++){
    nedge += neis[i].size();
    order[i] = -1;
  }
  nedge /= 2;

  while ( nedge > 0 ){
    /* disabled. It is available with c++17 and later.
    auto [newchain, cycle] = find_cycle(neis, chain);
    */
    //for c++14
    ArrayIntPair p = find_cycle(neis, chain, order);
    ArrayInt& newchain = p.first;
    ArrayInt& cycle    = p.second;
    // printArrayInt(cycle, 'o');
    cycles.push_back(cycle);
    chain.assign(newchain.begin(), newchain.end());
    remove_cycle(neis, cycle, order);
    nedge -= cycle.size();
  }
  return cycles;
}
