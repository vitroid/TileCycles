#include <vector>
#include <iostream>
#include <random>
#include <unistd.h>

using ArrayInt = std::vector< int >;
extern std::mt19937 gen;

void
printArrayInt(ArrayInt const& a, char c);

using ArrayArrayInt = std::vector< ArrayInt >;

ArrayArrayInt
tileByCycles(ArrayArrayInt& neis);
