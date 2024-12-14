import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import filedialog 
import os

class Sidebar(tk.Frame):
    def __init__(self, parent, task_manager, main_frame):
        super().__init__(parent)
        self.task_manager = task_manager
        self.main_frame = main_frame
        self.configure(bg="gray63")
        self.place(x=0, y=0, relwidth=0.28, relheight=1)

        self.create_widgets()
        self.layout_widgets()
        
    
        
        

    def create_widgets(self):
        self.title = tk.Label(self, text="TASK MANAGER", background="gray63", font=("Helvetica", 12, "bold"))
        self.task_name = tk.Label(self, text="Task name:", background="gray63", font=("Helvetica", 10, "bold"))
        self.name_entry = tk.Entry(self)
        self.priority = tk.Label(self, text="Priority:", background="gray63", font=("Helvetica", 10, "bold"))
        self.priority_combo = ttk.Combobox(self, values=["Low", "Medium", "High"])
        self.due_date = tk.Label(self, text="Due date:", background="gray63", font=("Helvetica", 10, "bold"))
        self.date_entry = DateEntry(self, selectmode="day", date_pattern="mm-dd-yyyy")
        self.add_task = tk.Button(self, text="Add task", background="dodgerblue2", command=self.on_add_task)
        self.export = tk.Button(self, text="Save", background="gray70", command=self.on_export)
        self.import_button = tk.Button(self, text="Load", background="gray70", command=self.on_import)  
        



    def layout_widgets(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 10), weight=1)
        self.rowconfigure(8, weight=25)

        self.title.grid(row=0, column=0, padx=20, pady=12, sticky="w")
        self.task_name.grid(row=1, column=0, padx=20, sticky="w")
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=8, sticky="nsew")
        self.priority.grid(row=3, column=0, padx=20, sticky="w")
        self.priority_combo.grid(row=4, column=0, columnspan=2, padx=20, pady=8, sticky="nsew")
        self.due_date.grid(row=5, column=0, padx=20, sticky="w")
        self.date_entry.grid(row=6, column=0, columnspan=2, padx=20, pady=8, sticky="nsew")
        self.add_task.grid(row=7, column=0, columnspan=2, padx=20, pady=8, sticky="ew")
        self.export.grid(row=9, column=0, columnspan=1, padx=20, pady=0, sticky="ew")
        self.import_button.grid(row=10, column=0, columnspan=1, padx=20, pady=8, sticky="ew") 


        

    def on_add_task(self):
        name = self.name_entry.get()
        priority = self.priority_combo.get()
        due_date = self.date_entry.get()

        if self.task_manager.add_task(name, priority, due_date):
            self.name_entry.delete(0, tk.END)
            self.priority_combo.set('')
            self.date_entry.set_date(datetime.now())
            self.main_frame.update_task_views()
        else:
            messagebox.showerror("Error", "Please fill in all task details")

    def on_export(self):
        export_filename = filedialog.asksaveasfilename(
            title="Save tasks as",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.path.expanduser("~/Documents")  
        )
        
        if export_filename: 
            print("Saving to:", export_filename) 
            exported_file = self.task_manager.export_tasks(export_filename)
            
            if exported_file:
                messagebox.showinfo("Export Successful", f"Tasks exported to {exported_file}")
            else:
                messagebox.showerror("Export Error", "There was an error exporting the tasks.")


    
    def on_import(self):  
        import_filename = filedialog.askopenfilename(title="Select a CSV file to import", filetypes=[("CSV files", "*.csv")])
        if import_filename:
            import_result = self.task_manager.import_tasks(import_filename)
            if import_result:
                messagebox.showinfo("Import Successful", f"Tasks imported from {import_filename}")
                self.main_frame.update_task_views()
            else:
                messagebox.showerror("Error", "Import failed or file is empty.")
                
    

class Main(ttk.Frame):
    def __init__(self, parent, task_manager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.place(relx=0.28, y=0, relwidth=0.72, relheight=1)
        
    
        self.sort_column_name = None
        self.sort_reverse = False 
        
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.search_entry = ttk.Entry(self)
        self.placeholder_text = "Search task id, name, or status (to search a specific task: id/name/status)"

        self.search_entry.insert(0, self.placeholder_text)
        self.search_entry.config(foreground="gray")

        self.search_entry.bind("<FocusIn>", self.on_entry_focus)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)
        
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
        self.update_button = tk.Button(self, text="Update", background="dodgerblue2", command=self.on_update_task)
        self.move_backward_button = tk.Button(self, text="Back", background="gray70", command=self.on_move_backward)
        
        self.refresh_button = tk.Button(self, text="Refresh", background="dodgerblue2", command=self.refresh)
        
    def on_entry_focus(self, event):
        if self.search_entry.get() == self.placeholder_text:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground="black")

    def on_entry_focus_out(self, event):

        if not self.search_entry.get():
            self.search_entry.insert(0, self.placeholder_text)
            self.search_entry.config(foreground="gray")
            
    

    def create_treeview(self, parent):
        treeview = ttk.Treeview(parent, columns=("Task Name", "Priority", "Due date", "Status"))

      
        treeview.column("#0", width=50, stretch=False)
        treeview.heading("#0", text="ID", anchor=tk.W, command=lambda: self.sort_column(treeview, "#0"))
        treeview.heading("Task Name", text="Task Name", anchor=tk.W, command=lambda: self.sort_column(treeview, "Task Name"))
        treeview.heading("Priority", text="Priority", anchor=tk.W, command=lambda: self.sort_column(treeview, "Priority"))
        treeview.heading("Due date", text="Due date", anchor=tk.W, command=lambda: self.sort_column(treeview, "Due date"))
        treeview.heading("Status", text="Status", anchor=tk.W, command=lambda: self.sort_column(treeview, "Status"))

    
        treeview.column("Task Name", width=150, stretch=True)
        treeview.column("Priority", width=100, stretch=False)
        treeview.column("Due date", width=100, stretch=False)
        treeview.column("Status", width=100, stretch=True)

        treeview.pack(side="left", fill="both", expand=True)
        return treeview

    def layout_widgets(self):
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=22)
        self.rowconfigure(2, weight=1)
        

        self.search_entry.grid(row=0, column=0, columnspan=3, padx=12, pady=12, sticky="ew")
        self.search_button.grid(row=0, column=3, padx=12, pady=12, sticky="ew")

        self.manager.grid(row=1, column=0, columnspan=4, padx=12, sticky="nsew")

        self.remove_button.grid(row=2, column=0, padx=12, pady=12, sticky="ew")
        self.update_button.grid(row=2, column=3, padx=12, pady=12, sticky="ew")
        self.move_backward_button.grid(row=2, column=2, padx=12, pady=12, sticky="ew")
        self.refresh_button.grid(row=2, column=1, padx=12, pady=12, sticky="ew") 


    def on_search(self):
        query = self.search_entry.get()
        results = self.task_manager.search_tasks(query)
        
        if not query or query == self.placeholder_text:
            return  

        for treeview in [self.task1, self.task2, self.task3, self.task4]:
            for item in treeview.get_children():
                treeview.delete(item)
                
        for task in results:
            task_id = task['id']
            task_name = task['name']
            task_priority = task['priority']
            task_due_date = task['due_date']
            task_status = task['status']

            self.task1.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))

            if task_status == "TO DO":
                self.task2.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))

            elif task_status == "IN PROGRESS":
                self.task3.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))

            elif task_status == "COMPLETED":
                self.task4.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))
                
                
                
                
                
                
                
                
                
                
                
            
    def on_remove_task(self):
        selected_tab_id = self.manager.select()
        if not selected_tab_id:
            messagebox.showwarning("Warning", "No tab selected.")
            return

        selected_tab = self.manager.nametowidget(selected_tab_id)
        
        treeview = None
        for widget in selected_tab.winfo_children():
            if isinstance(widget, ttk.Treeview):
                treeview = widget
                break

        if treeview is None:
            messagebox.showwarning("Warning", "Selected tab does not contain a Treeview.")
            return

        selected_items = treeview.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No task selected for removal.")
            return

        for item in selected_items:
            task_id = int(treeview.item(item)["text"])
            self.task_manager.remove_task(task_id)

        self.update_task_views()

    def sort_column(self, treeview, col):
        if col == self.sort_column_name:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False  
       
        self.sort_column_name = col

        
        items = [(treeview.set(item, col), item) for item in treeview.get_children('')]
        
    
        items.sort(key=lambda x: x[0], reverse=self.sort_reverse)
        
     
        for ix, item in enumerate(items):
            treeview.move(item[1], '', ix)
        
    
        treeview.heading(col, command=lambda: self.sort_column(treeview, col))

        
    def refresh(self):
        """ Refresh the task views by reloading and updating all tasks """
        self.update_task_views()   
        
        
        
        
        
        
    def on_update_task(self):
        selected_tab_id = self.manager.select()
        if not selected_tab_id:
            messagebox.showwarning("Warning", "No tab selected.")
            return

    
        selected_tab = self.manager.nametowidget(selected_tab_id)

        treeview = None
        for widget in selected_tab.winfo_children():
            if isinstance(widget, ttk.Treeview):
                treeview = widget
                break

        if treeview is None:
            messagebox.showwarning("Warning", "Selected tab does not contain a Treeview.")
            return

        selected_items = treeview.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No task selected for update.")
            return

        for item in selected_items:
            task_id = int(treeview.item(item)["text"])
            task = self.task_manager.get_task_by_id(task_id)
            if task is None:
                messagebox.showerror("Error", "Task not found.")
                return

            current_status = task['status']

            if current_status == "TO DO":
                new_status = "IN PROGRESS"
            elif current_status == "IN PROGRESS":
                new_status = "COMPLETED"
            elif current_status == "COMPLETED":
                new_status = "TO DO"
            else:
                messagebox.showerror("Error", "Invalid task status.")
                return

            self.task_manager.update_task_status(task_id, new_status)

        self.update_task_views() 
            
    
    def on_move_backward(self):
        selected_tab_id = self.manager.select() 
        if not selected_tab_id:
            messagebox.showwarning("Warning", "No tab selected.")
            return

        selected_tab = self.manager.nametowidget(selected_tab_id)

        treeview = None
        for widget in selected_tab.winfo_children():
            if isinstance(widget, ttk.Treeview):
                treeview = widget
                break

        if treeview is None:
            messagebox.showwarning("Warning", "Selected tab does not contain a Treeview.")
            return

        selected_items = treeview.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No task selected for status update.")
            return

        for item in selected_items:
            task_id = int(treeview.item(item)["text"])
            task = self.task_manager.get_task_by_id(task_id)
            if task is None:
                messagebox.showerror("Error", "Task not found.")
                return

            current_status = task['status']

    
            if current_status == "COMPLETED":
                new_status = "IN PROGRESS"
            elif current_status == "IN PROGRESS":
                new_status = "TO DO"
            elif current_status == "TO DO":
                messagebox.showinfo("Information", "Task is already at the earliest status.")
                return
            else:
                messagebox.showerror("Error", "Invalid task status.")
                return

            self.task_manager.update_task_status(task_id, new_status)

        self.update_task_views()
            
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def update_task_views(self):
        for treeview in [self.task1, self.task2, self.task3, self.task4]:
            for item in treeview.get_children():
                treeview.delete(item)

        all_tasks = self.task_manager.get_tasks()

        for task in all_tasks:
            task_id = task['id']
            task_name = task['name']
            task_priority = task['priority']
            task_due_date = task['due_date']
            task_status = task['status']

    
            self.task1.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))

    
            if task_status == "TO DO":
                self.task2.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))
            elif task_status == "IN PROGRESS":
                self.task3.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))
            elif task_status == "COMPLETED":
                self.task4.insert("", "end", text=task_id, values=(task_name, task_priority, task_due_date, task_status))