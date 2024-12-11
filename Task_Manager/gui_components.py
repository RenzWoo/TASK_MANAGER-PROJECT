import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

# GUI components


"""
Sidebar class is a tkinter Frame that represents the sidebar section of the task manager application, where the user interacts with task-related actions.
"""
class Sidebar(tk.Frame):
    # Initializes the sidebar with the parent container and connects the task manager backend.
    def __init__(self, parent, task_manager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.configure(bg="gray63")
        self.place(x=0, y=0, relwidth=0.28, relheight=1)

        self.create_widgets()
        self.layout_widgets()

    # Creates the widgets (buttons, labels, etc.) to be displayed on the sidebar.
    def create_widgets(self):
        # Create the widgets
        self.title = tk.Label(self, text="TASK MANAGER", background="gray63", font=("Helvetica", 12, "bold"))
        self.task_name = tk.Label(self, text="Task name:", background="gray63", font=("Helvetica", 10, "bold"))
        self.name_entry = tk.Entry(self)
        self.priority = tk.Label(self, text="Priority:", background="gray63", font=("Helvetica", 10, "bold"))
        self.priority_combo = ttk.Combobox(self, values=["Low", "Medium", "High"])
        self.due_date = tk.Label(self, text="Due date:", background="gray63", font=("Helvetica", 10, "bold"))
        self.date_entry = DateEntry(self, selectmode="day", date_pattern="mm-dd-yyyy")
        self.add_task = tk.Button(self, text="Add task", background="dodgerblue2", command=self.on_add_task)
        self.export = tk.Button(self, text="Export", background="gray70", command=self.on_export)

        # Create the grid
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure((0,10), weight=1)
        self.rowconfigure(8, weight=25)

    # Arranges the widgets in the sidebar according to a layout.
    def layout_widgets(self):
        self.title.grid(row=0, column=0, padx=20, pady=12, sticky="w")
        self.task_name.grid(row=1, column=0, padx=20, sticky="w")
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=8, sticky="nsew")
        self.priority.grid(row=3, column=0, padx=20, sticky="w")
        self.priority_combo.grid(row=4, column=0, columnspan=2, padx=20, pady=8, sticky="nsew")
        self.due_date.grid(row=5, column=0, padx=20, sticky="w")
        self.date_entry.grid(row=6, column=0, columnspan=2, padx=20, pady=8, sticky="nsew")
        self.add_task.grid(row=7, column=0, columnspan=2, padx=20, pady=8, sticky="ew")
        self.export.grid(row=9, column=0, columnspan=1, padx=20, pady=0, sticky="ew")

    # Handles the action for adding a new task.
    def on_add_task(self):
        name = self.name_entry.get()
        priority = self.priority_combo.get()
        due_date = self.date_entry.get()

        if self.task_manager.add_task(name, priority, due_date):
            self.name_entry.delete(0, tk.END)
            self.priority_combo.set('')
            self.date_entry.set_date(datetime.now())

            self.master.update_task_views()
        else:
            messagebox.showerror("Error", "Please fill in all task details")

    # Handles the task export action.
    def on_export(self):
        exported_file = self.task_manager.export_tasks()
        messagebox.showinfo("Export Successful", f"Tasks exported to {exported_file}")


"""
Main class is a ttk.Frame that represents the main content area of the task manager app, displaying task details, search functionality, and task management actions.
"""
class Main(ttk.Frame):
    # Initializes the main area with the parent container and task manager, setting up necessary components.
    def __init__(self, parent, task_manager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.place(relx=0.28, y=0, relwidth=0.72, relheight=1)

        self.create_widgets()
        self.layout_widgets()

    # Creates the widgets (buttons, entry fields, etc.) for the main content area.
    def create_widgets(self):
        self.search_entry = ttk.Entry(self)
        self.placeholder_text = "Search task id, name, or status (to search a specific task: id/name/status)"

        # Add placeholder text initially
        self.search_entry.insert(0, self.placeholder_text)
        self.search_entry.config(foreground="gray")

        # Add bindings for focus and text input
        self.search_entry.bind("<FocusIn>", self.on_entry_focus)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)

        # Add Search Button
        self.search_button = tk.Button(self, text="Search tasks", background="dodgerblue2", command=self.on_search)

        self.manager = ttk.Notebook(self)
        self.tab1 = tk.Frame(self.manager)
        self.tab2 = tk.Frame(self.manager)
        self.tab3 = tk.Frame(self.manager)
        self.tab4 = tk.Frame(self.manager)

        self.manager.add(self.tab1, text="ALL")
        self.manager.add(self.tab2, text="TO DO")
        self.manager.add(self.tab3, text="IN PROGRESS")
        self.manager.add(self.tab4, text="COMPLETED")

        self.task1 = self.create_treeview(self.tab1)
        self.task2 = self.create_treeview(self.tab2)
        self.task3 = self.create_treeview(self.tab3)
        self.task4 = self.create_treeview(self.tab4)

        self.remove_button = tk.Button(self, text="Remove task", background="gray70", command=self.on_remove_task)
        self.update_button = tk.Button(self, text="Update task", background="dodgerblue2", command=self.on_update_task)
        self.undo_button = tk.Button(self, text="Undo", background="gray70", command=self.on_undo_task)

    # Handles the focus event for task input fields.
    def on_entry_focus(self, event):
        # Remove placeholder text when the user focuses
        if self.search_entry.get() == self.placeholder_text:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground="black")

    # Handles the event when the task input field loses focus.
    def on_entry_focus_out(self, event):
        # Restore placeholder if the entry is empty
        if not self.search_entry.get():
            self.search_entry.insert(0, self.placeholder_text)
            self.search_entry.config(foreground="gray")

    # Creates a treeview widget for displaying tasks.
    def create_treeview(self, parent):
        treeview = ttk.Treeview(parent, columns=("Column 1", "Column 2", "Column 3"))
        treeview.heading("#0", text="ID", anchor=tk.W)
        treeview.heading("Column 1", text="Task name", anchor=tk.W)
        treeview.heading("Column 2", text="Priority", anchor=tk.W)
        treeview.heading("Column 3", text="Due date", anchor=tk.W)
        treeview.pack(side="left", fill="both", expand=True)
        return treeview

    # Organizes the widgets within the main section using a specific layout.
    def layout_widgets(self):
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=22)
        self.rowconfigure(2, weight=1)

        self.search_entry.grid(row=0, column=0, columnspan=3, padx=12, pady=12, sticky="ew")
        self.search_button.grid(row=0, column=3, padx=12, pady=12, sticky="ew")

        self.manager.grid(row=1, column=0, columnspan=4, padx=12, sticky="nsew")

        self.remove_button.grid(row=2, column=0, padx=12, pady=12, sticky="ew")
        self.undo_button.grid(row=2, column=2, padx=12, pady=12, sticky="ew")
        self.update_button.grid(row=2, column=3, padx=12, pady=12, sticky="ew")

    # Handles the task search action.
    def on_search(self):
        query = self.search_entry.get().strip()

        if not query:
            self.master.update_task_views()
            return

        results = self.task_manager.search_tasks(query)

        # Clear all treeviews
        for treeview in [self.task1, self.task2, self.task3, self.task4]:
            for item in treeview.get_children():
                treeview.delete(item)

        # Categorize results by status
        categorized_results = {
            None: [],  # For the ALL tab
            'TO DO': [],
            'IN PROGRESS': [],
            'COMPLETED': []
        }

        for task in results:
            categorized_results[None].append(task)  # Add to ALL
            categorized_results[task['status']].append(task)  # Add to specific status tab

        treeviews = [self.task1, self.task2, self.task3, self.task4]
        status_keys = [None, 'TO DO', 'IN PROGRESS', 'COMPLETED']

        for i, status in enumerate(status_keys):
            for task in categorized_results[status]:
                treeviews[i].insert('', 'end', text=task['id'],
                                    values=(task['name'], task['priority'], task['due_date']))

    # Handles the removal of a task.
    def on_remove_task(self):
        current_tab_index = self.manager.index(self.manager.select())
        treeviews = [self.task1, self.task2, self.task3, self.task4]
        current_treeview = treeviews[current_tab_index]

        selected_item = current_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to remove")
            return

        task_id = current_treeview.item(selected_item[0])['text']

        self.task_manager.remove_task(task_id)

        self.master.update_task_views()

    # Handles updating the details of an existing task.
    def on_update_task(self):
        current_tab_index = self.manager.index(self.manager.select())
        treeviews = [self.task1, self.task2, self.task3, self.task4]
        current_treeview = treeviews[current_tab_index]

        selected_item = current_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to update")
            return

        task_id = current_treeview.item(selected_item[0])['text']
        current_task = next((task for task in self.task_manager.tasks if task['id'] == task_id), None)

        if not current_task:
            messagebox.showerror("Error", "Task not found")
            return


        if current_task['status'] == 'COMPLETED':
            messagebox.showinfo("Update Blocked", "Task status is complete.")
            return

        status_cycle = ['TO DO', 'IN PROGRESS', 'COMPLETED']
        current_status = ['ALL', 'TO DO', 'IN PROGRESS', 'COMPLETED'][current_tab_index]

        if current_status == 'ALL':
            messagebox.showerror("Error", "Please select a specific status tab to update")
            return

        current_status_index = status_cycle.index(current_status)
        next_status = status_cycle[(current_status_index + 1) % len(status_cycle)]

        self.task_manager.update_task_status(task_id, next_status)

        self.master.update_task_views()

    # Handles the action for undoing a task-related operation (such as a status change).
    def on_undo_task(self):
        current_tab_index = self.manager.index(self.manager.select())
        treeviews = [self.task1, self.task2, self.task3, self.task4]
        current_treeview = treeviews[current_tab_index]

        selected_item = current_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to undo")
            return

        task_id = current_treeview.item(selected_item[0])['text']

        # Define the undo status cycle
        status_cycle = ['TO DO', 'IN PROGRESS', 'COMPLETED']
        current_status = ['ALL', 'TO DO', 'IN PROGRESS', 'COMPLETED'][current_tab_index]

        if current_status == 'ALL':
            messagebox.showerror("Error", "Please select a specific status tab to undo")
            return

        # Find the current task
        current_task = next((task for task in self.task_manager.tasks if task['id'] == task_id), None)

        if not current_task:
            messagebox.showerror("Error", "Task not found")
            return

        # Determine previous status
        if current_status == 'COMPLETED':
            previous_status = 'IN PROGRESS'
        elif current_status == 'IN PROGRESS':
            previous_status = 'TO DO'
        else:
            messagebox.showinfo("Cannot Undo", "Task is already at the first status")
            return

        # Update the task status
        self.task_manager.update_task_status(task_id, previous_status)

        self.master.update_task_views()
