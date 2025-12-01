#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <queue>
#include <set>
#include <map>
#include <iostream>

GrafoDisperso::GrafoDisperso() : num_nodos(0), num_aristas(0) {}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& filename) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
    std::cout << "[C++ Core] Cargando dataset '" << filename << "'..." << std::endl;

    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: No se pudo abrir el archivo " << filename << std::endl;
        return;
    }

    std::string line;
    std::vector<std::pair<int, int>> edges;
    int max_node_id = 0;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        int u, v;
        if (ss >> u >> v) {
            edges.push_back({u, v});
            if (u > max_node_id) max_node_id = u;
            if (v > max_node_id) max_node_id = v;
        }
    }
    file.close();

    num_nodos = max_node_id + 1;
    num_aristas = edges.size();

    // Convert to Adjacency List temporarily to sort and build CSR
    std::vector<std::vector<int>> adj(num_nodos);
    for (const auto& edge : edges) {
        adj[edge.first].push_back(edge.second);
        // Assuming directed graph based on typical web graphs, but if undirected, uncomment below:
        // adj[edge.second].push_back(edge.first); 
    }

    // Build CSR
    row_ptr.resize(num_nodos + 1);
    col_indices.reserve(num_aristas); // Approximate reservation
    
    int current_idx = 0;
    for (int i = 0; i < num_nodos; ++i) {
        row_ptr[i] = current_idx;
        // Sort neighbors for consistent CSR
        std::sort(adj[i].begin(), adj[i].end());
        for (int neighbor : adj[i]) {
            col_indices.push_back(neighbor);
            current_idx++;
        }
    }
    row_ptr[num_nodos] = current_idx;

    // Clean up temp memory
    // adj vector goes out of scope here

    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos << " | Aristas: " << num_aristas << std::endl;
    size_t memory_est = (row_ptr.size() * sizeof(int) + col_indices.size() * sizeof(int)) / (1024 * 1024);
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " << memory_est << " MB." << std::endl;
}

int GrafoDisperso::obtenerNodoMayorGrado() {
    int max_degree = -1;
    int max_node = -1;

    for (int i = 0; i < num_nodos; ++i) {
        int degree = row_ptr[i+1] - row_ptr[i];
        if (degree > max_degree) {
            max_degree = degree;
            max_node = i;
        }
    }
    return max_node;
}

std::vector<std::pair<int, int>> GrafoDisperso::BFS(int startNode, int depth) {
    std::cout << "[C++ Core] Ejecutando BFS nativo desde nodo " << startNode << " con profundidad " << depth << "..." << std::endl;
    std::vector<std::pair<int, int>> result_edges;
    
    if (startNode < 0 || startNode >= num_nodos) {
        std::cerr << "Error: Nodo de inicio fuera de rango." << std::endl;
        return result_edges;
    }

    std::queue<std::pair<int, int>> q; // node, current_depth
    std::set<int> visited;

    q.push({startNode, 0});
    visited.insert(startNode);

    while (!q.empty()) {
        int u = q.front().first;
        int d = q.front().second;
        q.pop();

        if (d >= depth) continue;

        int start_idx = row_ptr[u];
        int end_idx = row_ptr[u+1];

        for (int i = start_idx; i < end_idx; ++i) {
            int v = col_indices[i];
            
            // Add edge to result
            result_edges.push_back({u, v});

            if (visited.find(v) == visited.end()) {
                visited.insert(v);
                q.push({v, d + 1});
            }
        }
    }
    
    std::cout << "[C++ Core] Nodos encontrados (aristas): " << result_edges.size() << std::endl;
    return result_edges;
}

int GrafoDisperso::obtenerNumNodos() {
    return num_nodos;
}

int GrafoDisperso::obtenerNumAristas() {
    return num_aristas;
}
