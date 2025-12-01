import random

def generate_graph(filename, num_nodes, num_edges):
    print(f"Generating {filename} with {num_nodes} nodes and {num_edges} edges...")
    with open(filename, 'w') as f:
        for _ in range(num_edges):
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            if u != v:
                f.write(f"{u} {v}\n")
    print("Done.")

if __name__ == "__main__":
    generate_graph("data/large_graph.txt", 10000, 50000)
