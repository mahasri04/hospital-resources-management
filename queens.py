# queens.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class QueensTab:
    def __init__(self, app):
        self.app = app
        self.create_queens_tab()

    def create_queens_tab(self):
        self.tab = ttk.Frame(self.app.notebook)
        self.app.notebook.add(self.tab, text="Staff Scheduling")

        ttk.Label(self.tab, text="Staff Scheduling using 8 Queens Algorithm",
                 font=("Helvetica", 14, "bold")).pack(pady=10)

        explanation = ("This algorithm schedules staff to shifts without conflicts, "
                       "similar to placing queens on a chessboard without them attacking each other.")
        ttk.Label(self.tab, text=explanation, wraplength=600).pack(pady=5)

        control_frame = ttk.Frame(self.tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(control_frame, text="Generate Schedule", 
                   command=self.solve_queens_problem).pack()

        results_frame = ttk.Frame(self.tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.chessboard_frame = ttk.Frame(results_frame)
        self.chessboard_frame.pack()

        self.schedule_table = ttk.Treeview(results_frame, 
                                           columns=("Shift", "Doctor", "Nurse", "Technician"), 
                                           show="headings")
        self.schedule_table.heading("Shift", text="Shift")
        self.schedule_table.heading("Doctor", text="Doctor")
        self.schedule_table.heading("Nurse", text="Nurse")
        self.schedule_table.heading("Technician", text="Technician")

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.schedule_table.yview)
        self.schedule_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.schedule_table.pack(fill=tk.BOTH, expand=True)

    def is_safe(self, board, row, col):
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, 8, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True

    def solve_queens_util(self, board, col):
        if col >= 8:
            return True
        for i in range(8):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                if self.solve_queens_util(board, col + 1):
                    return True
                board[i][col] = 0
        return False

    def solve_queens_problem(self):
        board = [[0 for _ in range(8)] for _ in range(8)]
        if not self.solve_queens_util(board, 0):
            messagebox.showinfo("No Solution", "No solution exists for the 8 Queens problem")
            return
        self.display_chessboard(board)
        self.create_staff_schedule(board)

    def display_chessboard(self, board):
        for widget in self.chessboard_frame.winfo_children():
            widget.destroy()

        cell_size = 40
        queen_img = Image.open("queen.png") if os.path.exists("queen.png") else None
        if queen_img:
            queen_img = queen_img.resize((cell_size-5, cell_size-5))
            queen_photo = ImageTk.PhotoImage(queen_img)

        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                cell = tk.Frame(self.chessboard_frame, width=cell_size, height=cell_size,
                                bg=color, highlightthickness=1, highlightbackground="black")
                cell.grid(row=row, column=col)
                if board[row][col] == 1:
                    if queen_img:
                        label = tk.Label(cell, image=queen_photo, bg=color)
                        label.image = queen_photo
                        label.pack()
                    else:
                        tk.Label(cell, text="Q", bg=color, font=("Arial", 14)).pack()
        if queen_img:
            self.queen_images = queen_photo

    def create_staff_schedule(self, board):
        for item in self.schedule_table.get_children():
            self.schedule_table.delete(item)

        shifts = ["Morning", "Afternoon", "Night"]
        roles = ["Doctor", "Nurse", "Technician"]

        staff_by_role = {role: [s for s in self.app.staff if s["role"] == role] for role in roles}

        for col in range(8):
            shift = shifts[col % len(shifts)]
            day = (col // len(shifts)) + 1
            queen_row = [row for row in range(8) if board[row][col] == 1][0]
            assigned_staff = {}
            for role in roles:
                staff_list = staff_by_role.get(role, [])
                assigned_staff[role] = staff_list[queen_row % len(staff_list)]["name"] if staff_list else "None"

            self.schedule_table.insert("", tk.END, values=(
                f"Day {day} {shift}",
                assigned_staff["Doctor"],
                assigned_staff["Nurse"],
                assigned_staff["Technician"]
            ))