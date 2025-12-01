#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <iostream>

class GrafoDisperso : public GrafoBase {
private:
    int num_nodos;
    int num_aristas;
    
    // CSR Format
    std::vector<int> row_ptr;
    std::vector<int> col_indices;
    // We don't strictly need values for unweighted graph, but keeping it for completeness if needed later
    // std::vector<int> values; 

public:
    GrafoDisperso();
    ~GrafoDisperso();

    void cargarDatos(const std::string& filename) override;
    std::vector<std::pair<int, int>> BFS(int startNode, int depth) override;
    int obtenerNodoMayorGrado() override;
    int obtenerNumNodos() override;
    int obtenerNumAristas() override;
};

#endif // GRAFODISPERSO_H
