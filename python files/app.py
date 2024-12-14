import tkinter as tk
from task_manager import TaskManager
from ui_components import Sidebar, Main

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("1280x720")
        self.task_manager = TaskManager()
        self.main = Main(self, self.task_manager)
        self.sidebar = Sidebar(self, self.task_manager, self.main)
        
        self.main.update_task_views()
        self.iconbitmap("G:/School Stuff/2nd year/RATUNIL OOP/Final PIT/lebanana.ico") 
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
