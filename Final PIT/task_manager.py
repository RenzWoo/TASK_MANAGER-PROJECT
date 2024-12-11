import json
import os
import random
from datetime import datetime
import csv


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
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading tasks: {e}")
            return []

    def save_tasks(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def generate_unique_id(self):
        while True:
            task_id = random.randint(1735, 8025)
            if not any(task['id'] == task_id for task in self.tasks):
                return task_id

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
        if status is None:
            return self.tasks
        return [task for task in self.tasks if task['status'] == status]
    
    
   
    def get_task_by_id(self, task_id): 
        for task in self.tasks: 
            if task['id'] == task_id: 
                return task 
        return None  

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
        filtered_tasks = [task for task in self.tasks if query.lower() in task['name'].lower()]
        return filtered_tasks

    def export_tasks(self, file_path):
        try:
            with open(file_path, 'w') as f:
                f.write("ID,Name,Priority,Due Date,Status\n")
                for task in self.tasks:
                    safe_name = task['name'].replace(',', ';')
                    line = f"{task['id']},{safe_name},{task['priority']},{task['due_date']},{task['status']}\n"
                    f.write(line)
            return file_path  
        except IOError as e:
            print(f"Error exporting tasks: {e}")
            return None

        
    def update_task_details(self, task_id, name, priority, due_date):
        task = self.get_task_by_id(task_id)
        if task:
            task['name'] = name
            task['priority'] = priority
            task['due_date'] = due_date
            self.save_tasks()
            return True
        return False

    def import_tasks(self, import_filename='tasks_import.csv'):
        if not os.path.exists(import_filename):
            print(f"Error: File '{import_filename}' not found.")
            return False

        try:
            with open(import_filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        task = {
                            'id': int(row['ID']),
                            'name': row['Name'],
                            'priority': row['Priority'],
                            'due_date': row['Due Date'],
                            'status': row['Status']
                        }

                        if not any(task['id'] == t['id'] for t in self.tasks):
                            self.tasks.append(task)
                        else:
                            print(f"Task with ID {task['id']} already exists.")
                    except ValueError as e:
                        print(f"Error parsing task: {e}")
                        continue

            self.save_tasks() 
            return True
        except IOError as e:
            print(f"Error importing tasks: {e}")
            return False   