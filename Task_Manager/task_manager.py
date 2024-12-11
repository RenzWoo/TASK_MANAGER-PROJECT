import json
import os
from datetime import datetime

class Task:
    def __init__(self, task_name, priority, due_date):
        self.id = None
        self.name = task_name
        self.priority = priority
        self.due_date = due_date
        self.status = 'TO DO'

    def mark_completed(self):
        self.status = 'COMPLETED'

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def generate_unique_id(self):
        return len(self.tasks) + 1

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

    def get_tasks(self, status=None):
        # Filter tasks by status if specified
        filtered_tasks = [task for task in self.tasks if status is None or task['status'] == status]

        # Custom sorting function
        def task_sort_key(task):
            # Priority mapping to convert to numeric values for sorting
            priority_map = {
                'High': 3,
                'Medium': 2,
                'Low': 1
            }

            # Convert due date to datetime for comparison
            try:
                due_date = datetime.strptime(task['due_date'], '%m-%d-%Y')
            except ValueError:
                # If date parsing fails, use a far future date
                due_date = datetime(9999, 12, 31)

            # Return a tuple for sorting:
            # 1. Inverse priority (so High comes first)
            # 2. Due date (closer dates come first)
            return (
                -priority_map.get(task['priority'], 0),  # Negative to sort descending
                due_date
            )

        # Sort the filtered tasks
        return sorted(filtered_tasks, key=task_sort_key)

    def update_task_status(self, task_id, new_status):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = new_status
                self.save_tasks()
                return True
        return False

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()

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