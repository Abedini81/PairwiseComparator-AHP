import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Global variables
criteria = []
pairwise_matrix = None
weights = None

def get_criteria():
    global criteria, pairwise_matrix
    criteria_input = criteria_entry.get().strip()
    criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
    if len(criteria) < 2:
        messagebox.showerror("Error", "Please enter at least two criteria separated by commas.")
        return
    # Initialize pairwise matrix
    n = len(criteria)
    pairwise_matrix = np.zeros((n, n))
    np.fill_diagonal(pairwise_matrix, 1)
    build_pairwise_comparison_ui()

def build_pairwise_comparison_ui():
    global criteria
    # Clear previous frames
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    tk.Label(main_frame, text="Pairwise Comparison of Criteria", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

    row = 1
    entries = {}
    for i in range(len(criteria)):
        for j in range(i+1, len(criteria)):
            tk.Label(main_frame, text=f"Importance of {criteria[i]} compared to {criteria[j]}:", anchor="w").grid(row=row, column=0, sticky="w")
            entry = ttk.Entry(main_frame)
            entry.grid(row=row, column=1, padx=10, pady=5)
            entries[(i, j)] = entry
            row += 1

    def calculate_matrix():
        global pairwise_matrix
        try:
            for (i, j), entry in entries.items():
                value = float(entry.get())
                pairwise_matrix[i, j] = value
                pairwise_matrix[j, i] = 1 / value
            calculate_weights()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all comparisons.")

    tk.Button(main_frame, text="Calculate", command=calculate_matrix).grid(row=row, column=0, columnspan=2, pady=20)

def calculate_weights():
    global pairwise_matrix, weights
    # Normalize the matrix
    normalized_matrix = pairwise_matrix / pairwise_matrix.sum(axis=0)
    # Calculate weights
    weights = normalized_matrix.mean(axis=1)
    
    # Display results
    show_results()

def show_results():
    global criteria, pairwise_matrix, weights
    # Clear previous frames
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    tk.Label(main_frame, text="Pairwise Comparison Matrix:", font=("Arial", 14)).grid(row=0, column=0, pady=10, sticky="w")
    matrix_text = tk.Text(main_frame, height=10, width=50)
    matrix_text.insert("1.0", str(pairwise_matrix))
    matrix_text.grid(row=1, column=0, padx=10, pady=10)

    tk.Label(main_frame, text="Weights of Criteria:", font=("Arial", 14)).grid(row=2, column=0, pady=10, sticky="w")
    weights_text = tk.Text(main_frame, height=10, width=50)
    for i, weight in enumerate(weights):
        weights_text.insert("end", f"{criteria[i]}: {weight:.4f}\n")
    weights_text.grid(row=3, column=0, padx=10, pady=10)

    tk.Button(main_frame, text="Restart", command=restart_app).grid(row=4, column=0, pady=20)

def restart_app():
    global criteria, pairwise_matrix, weights
    criteria = []
    pairwise_matrix = None
    weights = None
    # Clear previous frames
    for widget in main_frame.winfo_children():
        widget.destroy()
    build_initial_ui()

def build_initial_ui():
    tk.Label(main_frame, text="Enter Decision Criteria (comma separated):", font=("Arial", 14)).grid(row=0, column=0, pady=10, sticky="w")
    global criteria_entry
    criteria_entry = ttk.Entry(main_frame, width=50)
    criteria_entry.grid(row=1, column=0, padx=10, pady=5)
    tk.Button(main_frame, text="Submit", command=get_criteria).grid(row=2, column=0, pady=20)

# Main application window
root = tk.Tk()
root.title("AHP Decision Support System")
root.geometry("600x600")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

build_initial_ui()

root.mainloop()
