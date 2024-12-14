## Task Manager Application

### Introduction
<p>This Python-based task manager application provides a user-friendly interface to create, manage, and track tasks. It provides features for adding, removing, updating, and searching tasks, while keeping track of their priority and due dates. It leverages the Tkinter library for the graphical user interface (GUI) and the tkcalendar library for date selection.</p>

### Features
1. **Create Tasks:** Add new tasks with descriptive names, set priorities (High, Medium, Low), and specify due dates.
2. **Task Statuses:** Track the progress of your tasks through various statuses: To Do, In Progress, and Completed.
3. **Organized Views:** Tasks are categorized and displayed in separate tabs based on their current status.
4. **Search Functionality:** Quickly locate specific tasks by filtering based on ID, name, or status information.
5. **Update Tasks:** Modify existing tasks by changing their details or updating their progress (e.g., marking "To Do" as "In Progress").
6. **Remove Tasks:** Delete tasks you no longer need.
7. **Persistence:** Task data is saved to a local file, ensuring your work is preserved even after you close the application.

### Installation
1. **Python Installation:**
    - Windows:<br>
        Download the latest Python installer from https://www.python.org/downloads/windows/ <br>
        During installation, ensure the "Add Python to PATH" option is checked. <br>
    - macOS: <br>
        Use Homebrew: brew install python <br>
    - Linux: <br>
        Use your system's package manager (e.g., apt, yum, dnf, pacman) to install Python. <br>
2. **Install Required Libraries** 
    - Using pip (Python's package installer): <br>
        Open your terminal or command prompt and run the following command: <br>
        **!pip install tkinter tkcalendar json os datetime** <br>
    - Using other package managers (e.g., conda): <br>
        Consult the documentation for your specific package manager for installation instructions. <br>

> **Note:** If you encounter any issues during installation, refer to the official documentation for each library or consult online resources for troubleshooting.

### Usage Instructions
1. **Add a Task:**<br>
    Enter a task name, priority, and due date.<br>
    Click the "Add task" button.<br>
2. **View Tasks:**<br>
    Tasks are categorized into "To Do," "In Progress," and "Completed" tabs.<br>
    Click on a tab to view tasks in that category.<br>
3. **Search Tasks:**<br>
    Enter a search query (e.g., task name, ID, or status) in the search bar.<br>
    Click the "Search tasks" button to filter the displayed tasks.<br>
4. **Update Tasks:**<br>
    Select a task to update.<br>
    Click the "Update task" button to change its status (e.g., from "To Do" to "In Progress").<br>
5. **Remove Tasks:**<br>
    Select a task to remove.<br>
    Click the "Remove task" button to delete the task.<br>

> **Additional Tips:** The application saves task data to a local file. You can export your tasks to a CSV file for backup or sharing.

## Enjoy using the Task Manager!
