#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <string>
#include <vector>
#include <utility>

class GrafoBase {
public:
    virtual ~GrafoBase() {}
    virtual void cargarDatos(const std::string& filename) = 0;
    virtual std::vector<std::pair<int, int>> BFS(int startNode, int depth) = 0;
    virtual int obtenerNodoMayorGrado() = 0;
    virtual int obtenerNumNodos() = 0;
    virtual int obtenerNumAristas() = 0;
};

#endif // GRAFOBASE_H
