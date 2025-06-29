# sorting.py
import tkinter as tk
from tkinter import ttk

class SortingTab:
    def __init__(self, app):
        self.app = app
        self.create_sorting_tab()

    def create_sorting_tab(self):
        self.tab = ttk.Frame(self.app.notebook)
        self.app.notebook.add(self.tab, text="Patient Prioritization")

        ttk.Label(self.tab, text="Patient Prioritization using Merge Sort", 
                 font=("Helvetica", 14, "bold")).pack(pady=10)

        control_frame = ttk.Frame(self.tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Sort By:").pack(side=tk.LEFT)
        self.sort_criteria = tk.StringVar(value="priority")

        ttk.Radiobutton(control_frame, text="Priority", variable=self.sort_criteria, 
                       value="priority").pack(side=tk.LEFT)
        ttk.Radiobutton(control_frame, text="Severity", variable=self.sort_criteria, 
                       value="severity").pack(side=tk.LEFT)
        ttk.Radiobutton(control_frame, text="Treatment Time", variable=self.sort_criteria, 
                       value="treatment_time").pack(side=tk.LEFT)

        ttk.Button(control_frame, text="Sort Patients", 
                  command=self.run_merge_sort).pack(side=tk.LEFT, padx=10)

        results_frame = ttk.Frame(self.tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("ID", "Name", "Condition", "Severity", "Priority", "Department", "Treatment Time")
        self.sorted_patient_table = ttk.Treeview(results_frame, columns=columns, show="headings")

        for col in columns:
            self.sorted_patient_table.heading(col, text=col)
            self.sorted_patient_table.column(col, width=100)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.sorted_patient_table.yview)
        self.sorted_patient_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sorted_patient_table.pack(fill=tk.BOTH, expand=True)

        self.update_sorted_patient_table(self.app.patients)

    def merge_sort(self, arr, key):
        if len(arr) > 1:
            mid = len(arr) // 2
            left = arr[:mid]
            right = arr[mid:]

            self.merge_sort(left, key)
            self.merge_sort(right, key)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i][key] > right[j][key]:  # Descending order
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1

    def run_merge_sort(self):
        criteria = self.sort_criteria.get()
        patients_copy = self.app.patients.copy()

        self.merge_sort(patients_copy, criteria)
        self.update_sorted_patient_table(patients_copy)

        for col in self.sorted_patient_table["columns"]:
            if col.lower() == criteria:
                self.sorted_patient_table.heading(col, text=f"{col} (Sorted)")
            else:
                self.sorted_patient_table.heading(col, text=col)

    def update_sorted_patient_table(self, patients):
        for item in self.sorted_patient_table.get_children():
            self.sorted_patient_table.delete(item)

        for patient in patients:
            self.sorted_patient_table.insert("", tk.END, values=(
                patient["id"], patient["name"], patient["condition"],
                patient["severity"], patient["priority"],
                patient["department"], f"{patient['treatment_time']} hours"
            ))
