import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Tkinter Table Example")

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Column 1", "Column 2", "Column 3"), show="headings")

# Configure the columns
tree.heading("Column 1", text="Column 1")
tree.heading("Column 2", text="Column 2")
tree.heading("Column 3", text="Column 3")

# Set the column widths
tree.column("Column 1", width=100)
tree.column("Column 2", width=100)
tree.column("Column 3", width=100)

# Insert sample data
tree.insert("", "end", values=("Data 1", "Data 2", "Data 3"))
tree.insert("", "end", values=("Data 4", "Data 5", "Data 6"))
tree.insert("", "end", values=("Data 7", "Data 8", "Data 9"))

# Pack the treeview widget
tree.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
