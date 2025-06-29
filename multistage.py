# multistage.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import heapq

class MultistageTab:
    def __init__(self, app):
        self.app = app
        self.create_multistage_tab()

    def create_multistage_tab(self):
        self.tab = ttk.Frame(self.app.notebook)
        self.app.notebook.add(self.tab, text="Patient Flow")

        ttk.Label(self.tab, text="Patient Flow Optimization using Multistage Graph",
                 font=("Helvetica", 14, "bold")).pack(pady=10)

        explanation = ("This algorithm finds the optimal path for patient flow through hospital departments "
                       "to minimize time and resource usage.")
        ttk.Label(self.tab, text=explanation, wraplength=600).pack(pady=5)

        control_frame = ttk.Frame(self.tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Start Department:").pack(side=tk.LEFT)
        self.start_dept = tk.StringVar()
        start_combo = ttk.Combobox(control_frame, textvariable=self.start_dept,
                                   values=list(self.app.departments.keys()))
        start_combo.current(0)
        start_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="End Department:").pack(side=tk.LEFT)
        self.end_dept = tk.StringVar()
        end_combo = ttk.Combobox(control_frame, textvariable=self.end_dept,
                                 values=list(self.app.departments.keys()))
        end_combo.current(1)
        end_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Find Optimal Path",
                   command=self.find_optimal_path).pack(side=tk.LEFT, padx=10)

        results_frame = ttk.Frame(self.tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.graph_canvas = tk.Canvas(results_frame, bg="white", width=600, height=300)
        self.graph_canvas.pack(fill=tk.BOTH, expand=True)

        self.path_output = scrolledtext.ScrolledText(results_frame, height=8)
        self.path_output.pack(fill=tk.BOTH, expand=True)

        self.initialize_graph_weights()
        self.draw_hospital_graph()

    def initialize_graph_weights(self):
        self.weights = {
            "ER": {"ICU": 3, "Radiology": 2, "General": 4},
            "ICU": {"ER": 3, "Surgery": 5},
            "Radiology": {"ER": 2, "Surgery": 3},
            "Surgery": {"ICU": 5, "Radiology": 3, "General": 2},
            "General": {"ER": 4, "Surgery": 2}
        }

    def draw_hospital_graph(self):
        self.graph_canvas.delete("all")
        self.node_positions = {
            "ER": (100, 150),
            "ICU": (300, 50),
            "Radiology": (300, 250),
            "Surgery": (500, 150),
            "General": (700, 150)
        }

        for dept, adjacents in self.weights.items():
            for adj, weight in adjacents.items():
                x1, y1 = self.node_positions[dept]
                x2, y2 = self.node_positions[adj]
                self.graph_canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="gray")
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                self.graph_canvas.create_text(mid_x, mid_y, text=str(weight), fill="black")

        for dept, (x, y) in self.node_positions.items():
            self.graph_canvas.create_oval(x-30, y-30, x+30, y+30, fill="#4ECDC4", outline="black")
            self.graph_canvas.create_text(x, y, text=dept, font=("Arial", 10, "bold"))

    def find_shortest_path(self, start, end):
        graph = self.weights
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        previous_nodes = {node: None for node in graph}
        priority_queue = [(0, start)]
        heapq.heapify(priority_queue)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue
            if current_node == end:
                break
            for neighbor, weight in graph.get(current_node, {}).items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()

        if not path or path[0] != start:
            return None, float('inf')

        return path, distances.get(end, float('inf'))

    def find_optimal_path(self):
        start = self.start_dept.get()
        end = self.end_dept.get()

        self.path_output.delete(1.0, tk.END)
        if start == end:
            self.path_output.insert(tk.END, "Start and end departments are the same!")
            return

        path, distance = self.find_shortest_path(start, end)
        if distance == float('inf'):
            self.path_output.insert(tk.END, "No valid path exists between these departments!\n")
            return

        self.path_output.insert(tk.END, f"Optimal Path from {start} to {end}:\n\n")
        self.path_output.insert(tk.END, f"Total Cost: {distance}\n\n")
        self.path_output.insert(tk.END, "Path:\n")
        self.path_output.insert(tk.END, " -> ".join(path) + "\n\n")
        self.highlight_path(path)

    def highlight_path(self, path):
        self.draw_hospital_graph()
        for i in range(len(path)-1):
            start = path[i]
            end = path[i+1]
            x1, y1 = self.node_positions[start]
            x2, y2 = self.node_positions[end]
            self.graph_canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="red", width=2)
            weight = self.weights[start][end]
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            self.graph_canvas.create_text(mid_x, mid_y, text=str(weight), fill="black")
