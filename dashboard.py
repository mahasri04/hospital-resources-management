# dashboard.py
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardTab:
    def __init__(self, app):
        self.app = app
        self.create_dashboard_tab()

    def create_dashboard_tab(self):
        self.tab = ttk.Frame(self.app.notebook)
        self.app.notebook.add(self.tab, text="Dashboard")

        ttk.Label(self.tab, text="Hospital Resource Dashboard", font=("Helvetica", 14, "bold")).pack(pady=10)

        summary_frame = ttk.Frame(self.tab)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)

        self.patient_count_label = ttk.Label(summary_frame, text="Total Patients: 0")
        self.patient_count_label.pack(side=tk.LEFT, padx=10)

        self.critical_patients_label = ttk.Label(summary_frame, text="Critical Patients: 0")
        self.critical_patients_label.pack(side=tk.LEFT, padx=10)

        self.bed_label = ttk.Label(summary_frame, text="Beds: 0/0")
        self.bed_label.pack(side=tk.LEFT, padx=10)

        self.staff_label = ttk.Label(summary_frame, text="Staff: 0/0")
        self.staff_label.pack(side=tk.LEFT, padx=10)

        vis_frame = ttk.Frame(self.tab)
        vis_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        fig1, ax1 = plt.subplots(figsize=(5, 3))
        self.patient_dist_chart = FigureCanvasTkAgg(fig1, vis_frame)
        self.patient_dist_chart.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        fig2, ax2 = plt.subplots(figsize=(5, 3))
        self.resource_util_chart = FigureCanvasTkAgg(fig2, vis_frame)
        self.resource_util_chart.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_dashboard(self):
        total_patients = len(self.app.patients)
        critical_patients = sum(1 for p in self.app.patients if p["severity"] >= 8)

        self.patient_count_label.config(text=f"Total Patients: {total_patients}")
        self.critical_patients_label.config(text=f"Critical Patients: {critical_patients}")

        beds = self.app.resources["beds"]
        nurses = self.app.resources["nurses"]
        self.bed_label.config(text=f"Beds: {beds['available']}/{beds['total']}")
        self.staff_label.config(text=f"Nurses: {nurses['available']}/{nurses['total']}")

        self.update_patient_distribution_chart()
        self.update_resource_utilization_chart()

    def update_patient_distribution_chart(self):
        fig = self.patient_dist_chart.figure
        fig.clear()
        ax = fig.add_subplot(111)

        departments = list(self.app.departments.keys())
        counts = [sum(1 for p in self.app.patients if p["department"] == dept) for dept in departments]

        ax.bar(departments, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
        ax.set_title("Patient Distribution by Department")
        ax.set_ylabel("Number of Patients")

        self.patient_dist_chart.draw()

    def update_resource_utilization_chart(self):
        fig = self.resource_util_chart.figure
        fig.clear()
        ax = fig.add_subplot(111)

        labels = ["Beds", "Nurses", "Doctors", "Medications"]
        used = [
            self.app.resources["beds"]["total"] - self.app.resources["beds"]["available"],
            self.app.resources["nurses"]["total"] - self.app.resources["nurses"]["available"],
            self.app.resources["doctors"]["total"] - self.app.resources["doctors"]["available"],
            1000 - self.app.resources["medications"]["available"]
        ]
        total = [
            self.app.resources["beds"]["total"],
            self.app.resources["nurses"]["total"],
            self.app.resources["doctors"]["total"],
            1000
        ]

        utilization = [used[i] / total[i] * 100 for i in range(len(labels))]
        ax.bar(labels, utilization, color=['#FFD166', '#06D6A0', '#118AB2', '#EF476F'])
        ax.set_title("Resource Utilization (%)")
        ax.set_ylim(0, 100)

        self.resource_util_chart.draw()
