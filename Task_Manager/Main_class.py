import tkinter as tk
from task_manager import TaskManager
from gui_components import Sidebar, Main

"""
A graphical user interface (GUI) application for managing tasks. 
It extends the tk.Tk class from the tkinter library, 
integrating task management functionality and 
UI components such as a sidebar and main area.
"""
class TaskManagerApp(tk.Tk):
    # Initializes the app window, sets up the task_manager(features & functionality), sidebar, and GUI components, and starts the event loop.
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        self.task_manager = TaskManager()

        self.sidebar = Sidebar(self, self.task_manager)
        self.main = Main(self, self.task_manager)

        self.update_task_views()
        self.mainloop()
    # Refreshes task views by clearing and updating the task lists in the main interface based on their status.
    def update_task_views(self):
        status_map = {
            'ALL': None,
            'TO DO': 'TO DO',
            'IN PROGRESS': 'IN PROGRESS',
            'COMPLETED': 'COMPLETED'
        }

        for tab_name, status in status_map.items():
            treeview = getattr(self.main, f'task{list(status_map.keys()).index(tab_name) + 1}')

            for item in treeview.get_children():
                treeview.delete(item)

            tasks = self.task_manager.get_tasks(status)
            for task in tasks:
                treeview.insert('', 'end', text=task['id'],
                                values=(task['name'], task['priority'], task['due_date']))