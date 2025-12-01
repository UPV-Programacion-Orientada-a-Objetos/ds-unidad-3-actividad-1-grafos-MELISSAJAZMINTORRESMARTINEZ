# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string
from neuronet cimport GrafoDisperso

cdef class PyGrafo:
    cdef GrafoDisperso* c_grafo

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def load_data(self, str filename):
        cdef string c_filename = filename.encode('utf-8')
        self.c_grafo.cargarDatos(c_filename)

    def bfs(self, int start_node, int depth):
        cdef vector[pair[int, int]] result = self.c_grafo.BFS(start_node, depth)
        # Convert C++ vector of pairs to Python list of tuples
        py_result = []
        for i in range(result.size()):
            py_result.append((result[i].first, result[i].second))
        return py_result

    def get_max_degree_node(self):
        return self.c_grafo.obtenerNodoMayorGrado()

    def get_num_nodes(self):
        return self.c_grafo.obtenerNumNodos()

    def get_num_edges(self):
        return self.c_grafo.obtenerNumAristas()
