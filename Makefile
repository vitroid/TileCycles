build_ext:
	python setup.py build_ext --inplace


test-cpp: test-cpp.o tilecycles.o
	clang++ $^ -o $@
%.o: %.cpp tilecycles.hpp
	clang++ -std=c++17 -c $< -g
