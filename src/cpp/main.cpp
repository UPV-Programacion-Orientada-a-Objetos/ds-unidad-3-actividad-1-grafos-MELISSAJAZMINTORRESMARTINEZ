#include "GrafoDisperso.h"
#include <iostream>

int main() {
    GrafoDisperso grafo;
    
    // Test loading
    grafo.cargarDatos("../../data/test_graph.txt");
    
    std::cout << "Nodes: " << grafo.obtenerNumNodos() << std::endl;
    std::cout << "Edges: " << grafo.obtenerNumAristas() << std::endl;
    
    // Test Max Degree
    int maxNode = grafo.obtenerNodoMayorGrado();
    std::cout << "Node with max degree: " << maxNode << std::endl;
    
    // Test BFS
    std::cout << "BFS from node 0, depth 2:" << std::endl;
    auto edges = grafo.BFS(0, 2);
    for (const auto& edge : edges) {
        std::cout << edge.first << " -> " << edge.second << std::endl;
    }
    
    return 0;
}
