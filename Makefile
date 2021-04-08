build_ext:
	python setup.py build_ext --inplace


test-cpp: test-cpp.o tilecycles.o c_tilecycles.o
	clang++ $^ -o $@
%.o: %.cpp tilecycles.hpp
	clang++ -std=c++17 -c $< -g `python3-config --includes` -I`python -c "import numpy; print(numpy.get_include())"`
