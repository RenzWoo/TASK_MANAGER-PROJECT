import json
import os
from tkinter import messagebox
from datetime import datetime

# Functionality (Implementations of features)

"""
The TaskManager class provides functionality for managing a collection of tasks. 
It handles task storage, retrieval, modification, and persistence, 
as well as utility features like exporting and searching tasks.
"""
class TaskManager:
    
    # Initializes the task manager by setting up a storage file (tasks.json by default) for tasks. Loads existing tasks from the file if it exists.
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    # Reads tasks from the JSON file and loads them into memory.
    def load_tasks(self):

        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    # Saves the current list of tasks to the JSON file.
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    # Generates a unique identifier(ID) for each task to prevent duplication.
    def generate_unique_id(self):
        return len(self.tasks) + 1

    # Adds a new task to the task list with specified details such as name, priority, and due date. Assigns a unique ID to the task.
    def add_task(self, name, priority, due_date):
        if not name or not priority or not due_date:
            return False

        task = {
            'id': self.generate_unique_id(),
            'name': name,
            'priority': priority,
            'due_date': due_date,
            'status': 'TO DO'
        }
        self.tasks.append(task)
        self.save_tasks()
        return True

    # Retrieves tasks based on their status ("TO DO", "IN PROGRESS", "COMPLETED"). Returns all tasks if no status is specified.
    def get_tasks(self, status=None):
        filtered_tasks = [task for task in self.tasks if status is None or task['status'] == status]

        def task_sort_key(task):
            priority_map = {
                'High': 3,
                'Medium': 2,
                'Low': 1
            }
            try:
                due_date = datetime.strptime(task['due_date'], '%m-%d-%Y')
            except ValueError:
                due_date = datetime(9999, 12, 31)
            return (-priority_map.get(task['priority'], 0), due_date)

        # Sort the filtered tasks
        return sorted(filtered_tasks, key=task_sort_key)

    # Updates the status of a specific task (identified by task_id) to a new status.
    def update_task_status(self, task_id, new_status):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = new_status
                self.save_tasks()
                return True
        return False

    # Removes a task from the task list based on its unique identifier.
    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()

    # Searches for tasks that match a given query string, potentially by name, priority, or other criteria.
    def search_tasks(self, query):
        # If query is empty, return an empty list
        if not query:
            return []

        # Split the query and convert to lowercase for case-insensitive search
        search_terms = [term.strip().lower() for term in query.split('/')]

        # Function to check if any search term matches the task
        def match_task(task):
            for term in search_terms:
                # Check if the term matches task name, id, or status
                if (term in str(task['id']).lower() or
                        term in task['name'].lower() or
                        term in task['status'].lower()):
                    return True
            return False

        # Return tasks that match any of the search terms
        return [task for task in self.tasks if match_task(task)]
    
    # Exports the list of tasks to an external file or format for sharing or backup purposes.
    def export_tasks(self):
        export_filename = 'tasks_export.csv'

        with open(export_filename, 'w') as f:
            f.write("ID,Name,Priority,Due Date,Status\n")

            for task in self.tasks:
                safe_name = task['name'].replace(',', ';')

                line = f"{task['id']},{safe_name},{task['priority']},{task['due_date']},{task['status']}\n"
                f.write(line)

        full_path = os.path.abspath(export_filename)
        messagebox.showinfo("Export Successful", f"Tasks exported to:\n{full_path}")

        return full_path