import tkinter as tk
from task_manager import TaskManager
from ui_components import Sidebar, Main

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("800x600")
        self.task_manager = TaskManager()
        self.main = Main(self, self.task_manager)
        self.sidebar = Sidebar(self, self.task_manager, self.main)
        
        self.main.update_task_views() 
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
