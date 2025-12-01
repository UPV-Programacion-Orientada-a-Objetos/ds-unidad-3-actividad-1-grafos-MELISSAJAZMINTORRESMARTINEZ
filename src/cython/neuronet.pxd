from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string

cdef extern from "../cpp/GrafoBase.h":
    pass

cdef extern from "../cpp/GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        void cargarDatos(string filename)
        vector[pair[int, int]] BFS(int startNode, int depth)
        int obtenerNodoMayorGrado()
        int obtenerNumNodos()
        int obtenerNumAristas()
