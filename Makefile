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


test-deploy: build
	twine upload -r pypitest dist/*
test-install:
	pip install --index-url https://test.pypi.org/simple/ $(PKGNAME)

pep8:
	autopep8 -r -a -a -i .

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
