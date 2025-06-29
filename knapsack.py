# knapsack.py
import tkinter as tk
from tkinter import ttk, scrolledtext

class KnapsackTab:
    def __init__(self, app):
        self.app = app
        self.create_knapsack_tab()

    def create_knapsack_tab(self):
        self.tab = ttk.Frame(self.app.notebook)
        self.app.notebook.add(self.tab, text="Resource Allocation")

        ttk.Label(self.tab, text="Fractional Knapsack for Resource Allocation",
                  font=("Helvetica", 14, "bold")).pack(pady=10)

        control_frame = ttk.Frame(self.tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Resource Type:").pack(side=tk.LEFT)
        self.resource_type = tk.StringVar()
        resource_combo = ttk.Combobox(control_frame, textvariable=self.resource_type,
                                      values=["Beds", "Nurses", "Doctors", "Medications"])
        resource_combo.current(0)
        resource_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Available Units:").pack(side=tk.LEFT)
        self.resource_units = tk.IntVar(value=15)
        ttk.Entry(control_frame, textvariable=self.resource_units, width=5).pack(side=tk.LEFT)

        ttk.Button(control_frame, text="Allocate Resources",
                   command=self.run_knapsack).pack(side=tk.LEFT, padx=10)

        results_frame = ttk.Frame(self.tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("ID", "Name", "Condition", "Severity", "Priority", "Resource Need")
        self.patient_table = ttk.Treeview(results_frame, columns=columns, show="headings")

        for col in columns:
            self.patient_table.heading(col, text=col)
            self.patient_table.column(col, width=100)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.patient_table.yview)
        self.patient_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.patient_table.pack(fill=tk.BOTH, expand=True)

        output_frame = ttk.LabelFrame(self.tab, text="Allocation Results")
        output_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        self.knapsack_output = scrolledtext.ScrolledText(output_frame, height=8)
        self.knapsack_output.pack(fill=tk.BOTH, expand=True)

        self.update_patient_table()

    def update_patient_table(self):
        for item in self.patient_table.get_children():
            self.patient_table.delete(item)

        for patient in self.app.patients:
            resource_type = self.resource_type.get().lower()
            resource_need = patient["resources_needed"].get(resource_type[:-1], 0)
            self.patient_table.insert("", tk.END, values=(
                patient["id"], patient["name"], patient["condition"],
                patient["severity"], patient["priority"], resource_need
            ))

    def fractional_knapsack(self, capacity, items):
        items.sort(key=lambda x: x["priority"] / x["weight"], reverse=True)
        total_value = 0.0
        selected_items = []

        for item in items:
            if capacity >= item["weight"]:
                selected_items.append({"item": item, "fraction": 1.0})
                total_value += item["priority"]
                capacity -= item["weight"]
            else:
                fraction = capacity / item["weight"]
                selected_items.append({"item": item, "fraction": fraction})
                total_value += item["priority"] * fraction
                break

        return total_value, selected_items

    def run_knapsack(self):
        resource_type = self.resource_type.get().lower()
        capacity = self.resource_units.get()

        items = []
        for patient in self.app.patients:
            need = patient["resources_needed"].get(resource_type[:-1], 0)
            if need > 0:
                items.append({
                    "patient": patient,
                    "weight": need,
                    "priority": patient["priority"]
                })

        if not items:
            self.knapsack_output.delete(1.0, tk.END)
            self.knapsack_output.insert(tk.END, "No patients require this resource type.")
            return

        total_value, selected_items = self.fractional_knapsack(capacity, items)

        self.knapsack_output.delete(1.0, tk.END)
        self.knapsack_output.insert(tk.END, f"Resource Allocation Results for {resource_type.capitalize()}\n\n")
        self.knapsack_output.insert(tk.END, f"Total Available Units: {capacity}\n")
        self.knapsack_output.insert(tk.END, f"Total Priority Score Achieved: {total_value:.2f}\n\n")
        self.knapsack_output.insert(tk.END, "Allocation Details:\n")

        total_units_used = 0
        for allocation in selected_items:
            item = allocation["item"]
            fraction = allocation["fraction"]
            units = item["weight"] * fraction
            self.knapsack_output.insert(tk.END,
                f"- {item['patient']['name']} ({item['patient']['condition']}): {units:.1f}/{item['weight']} units (Priority: {item['priority']})\n")
            total_units_used += units

        self.knapsack_output.insert(tk.END, f"\nTotal Units Used: {total_units_used:.1f}/{capacity}\n")
        self.knapsack_output.insert(tk.END, f"Utilization Rate: {total_units_used / capacity * 100:.1f}%")
