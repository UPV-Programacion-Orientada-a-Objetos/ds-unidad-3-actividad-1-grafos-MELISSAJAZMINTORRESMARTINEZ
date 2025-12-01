import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

# Add project root to sys.path to find neuronet extension
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import neuronet
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet: Análisis de Grafos Masivos")
        self.root.geometry("1000x800")

        self.grafo = None

        # --- Sidebar ---
        self.sidebar = tk.Frame(root, width=250, bg="#f0f0f0", padx=10, pady=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Load Section
        tk.Label(self.sidebar, text="Dataset", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(0, 5), anchor="w")
        self.btn_load = tk.Button(self.sidebar, text="Cargar Archivo de Grafo", command=self.load_file)
        self.btn_load.pack(fill=tk.X, pady=5)

        # Metrics Section
        tk.Label(self.sidebar, text="Métricas", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(20, 5), anchor="w")
        self.lbl_nodes = tk.Label(self.sidebar, text="Nodos: -", bg="#f0f0f0", anchor="w")
        self.lbl_nodes.pack(fill=tk.X)
        self.lbl_edges = tk.Label(self.sidebar, text="Aristas: -", bg="#f0f0f0", anchor="w")
        self.lbl_edges.pack(fill=tk.X)
        self.lbl_max_degree = tk.Label(self.sidebar, text="Nodo Mayor Grado: -", bg="#f0f0f0", anchor="w")
        self.lbl_max_degree.pack(fill=tk.X)

        # Analysis Section
        tk.Label(self.sidebar, text="Análisis", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(20, 5), anchor="w")
        
        tk.Label(self.sidebar, text="Nodo Inicial:", bg="#f0f0f0").pack(anchor="w")
        self.entry_start_node = tk.Entry(self.sidebar)
        self.entry_start_node.pack(fill=tk.X)
        
        tk.Label(self.sidebar, text="Profundidad:", bg="#f0f0f0").pack(anchor="w")
        self.entry_depth = tk.Entry(self.sidebar)
        self.entry_depth.insert(0, "2")
        self.entry_depth.pack(fill=tk.X)

        self.btn_bfs = tk.Button(self.sidebar, text="Ejecutar BFS y Visualizar", command=self.run_bfs)

        self.btn_bfs.pack(fill=tk.X, pady=10)

        # --- Main Area ---
        self.main_area = tk.Frame(root, bg="white")
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_area)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")])
        if not file_path:
            return

        try:
            self.grafo = neuronet.PyGrafo()
            # Use relative path if possible for cleaner logs, or absolute
            self.grafo.load_data(file_path)
            
            num_nodes = self.grafo.get_num_nodes()
            num_edges = self.grafo.get_num_edges()
            max_degree_node = self.grafo.get_max_degree_node()

            self.lbl_nodes.config(text=f"Nodos: {num_nodes}")
            self.lbl_edges.config(text=f"Aristas: {num_edges}")
            self.lbl_max_degree.config(text=f"Nodo Mayor Grado: {max_degree_node}")
            
            messagebox.showinfo("Éxito", f"¡Grafo cargado exitosamente!\nNodos: {num_nodes}\nAristas: {num_edges}")

        except Exception as e:
            messagebox.showerror("Error", f"Fallo al cargar el grafo: {e}")

    def run_bfs(self):
        if not self.grafo:
            messagebox.showwarning("Advertencia", "Por favor cargue un grafo primero.")
            return

        try:
            start_node = int(self.entry_start_node.get())
            depth = int(self.entry_depth.get())
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para Nodo Inicial o Profundidad.")
            return

        try:
            edges = self.grafo.bfs(start_node, depth)
            
            self.ax.clear()
            
            if not edges:
                self.ax.text(0.5, 0.5, "No se encontraron aristas o el nodo está aislado.", ha='center')
                self.canvas.draw()
                return

            # Visualize with NetworkX
            G = nx.Graph() # Or DiGraph if directed
            G.add_edges_from(edges)
            
            pos = nx.spring_layout(G, seed=42)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, ax=self.ax, node_size=300, node_color='skyblue')
            # Draw edges
            nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='gray')
            # Draw labels
            nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=10)
            
            # Highlight start node
            if start_node in G.nodes:
                nx.draw_networkx_nodes(G, pos, ax=self.ax, nodelist=[start_node], node_color='red', node_size=400)

            self.ax.set_title(f"Resultado BFS (Inicio: {start_node}, Profundidad: {depth})")
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"BFS falló: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()
