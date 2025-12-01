import neuronet
import os

def test_neuronet():
    print("Testing NeuroNet Cython Extension...")
    grafo = neuronet.PyGrafo()
    
    data_path = "data/test_graph.txt"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    print(f"Loading {data_path}...")
    grafo.load_data(data_path)
    
    print(f"Nodes: {grafo.get_num_nodes()}")
    print(f"Edges: {grafo.get_num_edges()}")
    print(f"Max Degree Node: {grafo.get_max_degree_node()}")
    
    print("BFS from 0, depth 2:")
    edges = grafo.bfs(0, 2)
    for u, v in edges:
        print(f"{u} -> {v}")

if __name__ == "__main__":
    test_neuronet()
