import tkinter as tk
from tkinter import ttk
from dashboard import DashboardTab
from knapsack import KnapsackTab
from sorting import SortingTab
from queens import QueensTab
from multistage import MultistageTab
from utils import generate_patients, generate_resources, generate_staff, generate_departments

class HospitalResourceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Hospital Resource Management System")
        self.root.geometry("1200x800")

        # Initialize data
        self.patients = generate_patients()
        self.resources = generate_resources()
        self.staff = generate_staff()
        self.departments = generate_departments()

        # Create Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Initialize Tabs
        self.dashboard_tab = DashboardTab(self)
        self.knapsack_tab = KnapsackTab(self)
        self.sorting_tab = SortingTab(self)
        self.queens_tab = QueensTab(self)
        self.multistage_tab = MultistageTab(self)

        # Update dashboard initially
        self.dashboard_tab.update_dashboard()
