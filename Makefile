PKGNAME=tilecycles


build_ext:
	python setup.py build_ext --inplace


test-cpp: test-cpp.o tilecycles_c.o
	clang++ $^ -o $@
%.o: %.cpp tilecycles_c.hpp
	clang++ -std=c++17 -c $< -g `python3-config --includes` -I`python -c "import numpy; print(numpy.get_include())"`
benchmark:
	python benchmark.py

%: temp_% replacer.py $(wildcard *.py *.c)
	pip install genice2_dev
	python replacer.py < $< > $@


test-deploy:
	poetry publish --build -r testpypi
test-install:
	pip install --index-url https://test.pypi.org/simple/ $(PKGNAME)
uninstall:
	-pip uninstall -y $(PKGNAME)
build: README.md $(wildcard cycles/*.py)
	poetry build
deploy:
	poetry publish --build
check:
	poetry check




clean:
	-rm $(ALL) *.so *~ */*~ *.o *.gro *.rdf
	-rm -rf build dist *.egg-info
	# -rm -rf PairList.egg-info
