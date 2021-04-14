PKGNAME=tilecycles


build_ext:
	python setup.py build_ext --inplace


test-cpp: test-cpp.o tilecycles.o c_tilecycles.o
	clang++ $^ -o $@
%.o: %.cpp tilecycles.hpp
	clang++ -std=c++17 -c $< -g `python3-config --includes` -I`python -c "import numpy; print(numpy.get_include())"`


%: temp_% replacer.py $(wildcard *.py *.c)
	pip install genice2_dev
	python replacer.py < $< > $@


test-deploy: build
	twine upload -r pypitest dist/*
test-install:
	pip install --index-url https://test.pypi.org/simple/ $(PKGNAME)


install:
	python setup.py install
uninstall:
	-pip uninstall -y $(PKGNAME)
build: README.md
	./setup.py sdist # bdist_wheel


deploy: build
	twine upload --repository pypi dist/*
check:
	./setup.py check


clean:
	-rm $(ALL) *.so *~ */*~ *.o *.gro *.rdf
	-rm -rf build dist *.egg-info
	# -rm -rf PairList.egg-info
