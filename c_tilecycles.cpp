/*
 * Interface to c++ tilecycles.
 */
#include <Python.h>
//#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
//#include "C_arraytest.h"
#include <math.h>
#include "tilecycles.hpp"

static PyObject *tile(PyObject *self, PyObject* args);

std::mt19937 gen;

static PyMethodDef module_methods[] = {
  {"tile", tile, METH_VARARGS,
   "Tile the undirected even graph by cycles.\n"
   "Input:\n"
   "pairs\tA numpy 2D array of size Nedge x2.\n"
   "Nnode\tNumber of nodes in the graph. The values in pairs must be less than it.\n"
   "seed\tRandom seed.\n"
   "Output:\n"
   "A list of cycle members.\n"},
  {NULL, NULL, 0, NULL}};

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "tilecycles",
        NULL,
        -1,
        module_methods,
        NULL,
        NULL,
        NULL,
        NULL
};


//my initializer
PyMODINIT_FUNC PyInit_tilecycles(void) {
  PyObject *m;
  import_array();
  m = PyModule_Create(&moduledef);
  if (!m)
    return NULL;
  return m;
}




/* ==== Check that PyArrayObject is a double (Float) type and a matrix ==============
    return 1 if an error and raise exception */
int not_intmatrix(PyArrayObject *mat)  {
	if (mat->descr->type_num != NPY_INT32 || mat->nd != 2)  {
		PyErr_SetString(PyExc_ValueError,
			"In not_intmatrix: array must be of type Int32 and 2 dimensional (n x m).");
		return 1;  }
	return 0;
}

static PyObject *tile(PyObject *self, PyObject* args) {
  // expect two arguments.
  PyArrayObject *pairs;
  int Nnode, seed;
  //int dimss[2], ngrid[3];

  /* Parse tuples separately since args will differ between C fcns */
  if (!PyArg_ParseTuple(args, "O!ii", &PyArray_Type,
			&pairs, &Nnode, &seed)) return NULL;
  //if (!PyArg_ParseTuple(args, "I", &n, &m, &ngrid[0], &ngrid[1], &ngrid[2])) return NULL;
  if (NULL == pairs) return NULL;
  if (not_intmatrix(pairs)) return NULL;
  if ( pairs->dimensions[1] != 2 ) return NULL;
  gen.seed(seed);

  /* Get the dimensions of the input */
  int npairs =pairs->dimensions[0];
  //int m=dimss[1]=rpos->dimensions[1];

  int* a = (int*)pairs->data;

  //neisを構成する。
  ArrayArrayInt neis(Nnode);
  for(auto i=0L; i<npairs*2; i+=2){
    int x=a[i];
    int y=a[i+1];
    neis[x].push_back(y);
    neis[y].push_back(x);
  }

  for(auto i=0L; i<Nnode; i++){
    if ( neis[i].size() % 2 != 0 ){
      PyErr_SetString(PyExc_ValueError,
  			"The graph is not an even graph.");
  		return NULL;
    }
  }
  ArrayArrayInt cycles = tileByCycles(neis);
  //std::cout << sizeof(int) << " int" << std::endl;
  //int is 4-byte 32 bit!
  //値をどうやって返すか。
  //理想的なのはarrayのlistかlistのlist。
  //それが無理なら、arrayと見出しarray。
  //https://mail.python.org/pipermail/tutor/2005-February/035686.html

  PyObject* pylist = PyTuple_New(cycles.size());
  for(unsigned int i=0; i<cycles.size(); i++){
    // allocate and make a disposable copy
    auto asize = sizeof(int)*cycles[i].size();
    int* cycle_data = (int*) malloc(asize);
    for(unsigned int  j=0; j<cycles[i].size(); j++){
      cycle_data[j] = cycles[i][j];
      // std::cout << cycle_data[j] << " ";
    }
    // std::cout << std::endl;
    // Make it a 1-dim numpy array of int
    npy_intp dims[1] = {static_cast<npy_intp>(cycles[i].size())};
    PyObject* cycle = PyArray_SimpleNewFromData(1, dims, NPY_INT32, cycle_data);
    // this is the critical line - tell numpy it has to free the data
    PyArray_ENABLEFLAGS((PyArrayObject*)cycle, NPY_ARRAY_OWNDATA);
    // and put it in the list
    PyTuple_SetItem(pylist, i, cycle);
  }
  return pylist;
}
