import json
import os

# --- Constants ---
# Define the filename where tasks will be stored
TASKS_FILE = 'tasks.json'
TRASH_FILE = 'trash.json'

# --- Data Loading/Saving Functions ---

def load_tasks():
    """
    Loads tasks from the TASKS_FILE.
    If the file doesn't exist, return an empty list.
    """
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        try:
            # Load existing tasks; ensure it's a list
            tasks = json.load(f)
            if not isinstance(tasks, list):
                print(f"Warning: {TASKS_FILE} content is not a list. Resetting tasks.")
                return []
            return tasks
        except json.JSONDecodeError:
        # Handle empty or malformed JSON file
            print(f"Error reading {TASKS_FILE}. Starting with an empty task list.")
            return []
        
def load_trash():
    """
    Loads trash from the TRASH.
    If the file doesn't exist, return an empty list.
    """
    if not os.path.exists(TRASH_FILE):
        return []
    with open(TRASH_FILE, 'r') as f:
        try:
            # Load existing trash; ensure it's a list
            trash = json.load(f)
            if not isinstance(trash, list):
                return []
            return trash
        except json.JSONDecodeError:
            return []
  
def save_tasks(tasks):
    """Saves the current list of tasks to the TASKS_FILE."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4) # indent=4 makes the JSON file human-readable

 # --- Core To-Do List Functions ---

def display_tasks(tasks):
    """Displays all tasks with their status and index."""
    if not tasks:
        print("\nYour to-do list is empty! Time to add some tasks.")
        return

    print("\n--- Your To-Do List ---")
    for i, task in enumerate(tasks):
        status = "✓" if task['completed'] else " "
        print(f"{i + 1}. [{status}] {task['description']}")
    print("-----------------------\n")

def add_task(tasks):
    """Prompts the user for a task description and adds it to the list."""
    description = input("Enter the new task description: ").strip()
    if description:
        tasks.append({'description': description, 'completed': False})
        print(f"Task '{description}' added.")
    else:
      print("Task description cannot be empty.")

def mark_task_complete(tasks):
    """Allows the user to mark a task as complete by its index."""
    display_tasks(tasks)
    if not tasks:
        return

    try:
        task_num = int(input("Enter the number of the task to mark as complete: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]['completed'] = True
            save_tasks(tasks)
            print(f"Task {task_num} marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task(tasks, trash):
    """Allows the user to delete a task by its index."""
    display_tasks(tasks)
    if not tasks:
        return

    try:
        task_num = int(input("Enter the number of the task to delete: "))
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f"Task '{removed_task['description']}' deleted.")
            trash.append(removed_task)
            save_tasks(trash)
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def prioritize_task(tasks):
    """Allows the user to add priority levels to the task"""
    display_tasks(tasks)
    if not tasks:
        return
    
    try:
        task_num = int(input("Enter the number of the task to prioritize: "))
        if 1 <= task_num <= len(tasks):
            hold_task = tasks.pop(task_num -1)
            tasks.insert(0,hold_task)
            save_tasks(tasks)
            print(f"Task '{hold_task['description']}' moved to top.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")
    
def filter_task(tasks):
    """Allows the user to filter tasks by status (only incomplete tasks)."""
    print(f"Displaying only incomplete tasks.\n")
    for i, task in enumerate(tasks):
        if not task['completed']:
            print(f"{i + 1}. [ ] {task['description']}")
    print("----------------------------\n")
        
def Search_task(tasks):
    """Allows the user to search for tasks."""
    
    try:
        searchDescription = input("Enter the task description to search: ").strip()
        for i, task in enumerate(tasks):
            if searchDescription in task["description"]:
                status = "✓" if task['completed'] else " "
                print(f"{i + 1}. [{status}] {task['description']}")
    except Exception:
        # A except that return unfound task
        print("Task description not found!")
    finally:
        print("\nTask found!")

def edit_task(tasks):
    """Allows the user to edit task description"""
    display_tasks(tasks)
    
    try:
        task_num = int(input("Enter the number of the task to edit: "))
        new_description = input("Enter the new task description: ").strip()
        if new_description:

            tasks[task_num -1]['description'] = new_description
            tasks[task_num -1]['completed'] = False
            save_tasks(tasks)
            print(f"Task '{new_description}' changed.")
        else:
            print("Task description cannot be empty.")
    except ValueError:
        print("Please enter a valid number.")
    finally:
        display_tasks(tasks)
        
def undo_task(tasks, trash):
    """Allows the user to undo 'mark task as complete', 'delete', 'add' tasks"""
    if not tasks:
        return

    while True:
        print("\n === Choose Task to undo ===")
        print("1. Undo delete task")
        print("2. Undo mark task as complete")
        print("3. Exit undo task.")

        choice = input("Enter your choice: ")

        if choice == '1':
            if trash:
                print("\nRestoring last deleted task!")
                removed_trash = trash.pop(0)
                tasks.append(removed_trash)
                save_tasks(tasks)
                save_tasks(trash)
                print(f"Task '{removed_trash['description']}' restored")
            else:
                print(f"\nThere are no task to restore!")
        elif choice == '2':
            display_tasks(tasks)
            try:
                task_num = int(input("Enter the number of the task to mark as incomplete: "))
                if 1 <= task_num <= len(tasks):
                    tasks[task_num - 1]['completed'] = False
                    save_tasks(tasks)
                    print(f"Task {task_num} marked as incomplete.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '3':
            print("Exiting Undo task.")
            break
        else:
            print("Invalid choice. Please try again.")

    
# --- Main Application Logic ---

def main():
    """Main function to run the To-Do List application."""
    tasks = load_tasks() # Load tasks at the start
    trash = load_trash() # Load trash at the start
    
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Veiw Tasks")
        print("2. Add Task")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Prioritize Task")
        print("6. Filter Task")
        print("7. Search Task")
        print("8. Edit Task")
        print("9. Undo Task")
        print("10. Exit")
        print("-------------------------")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            mark_task_complete(tasks)
        elif choice == '4':
            delete_task(tasks, trash)
        elif choice == '5':
            prioritize_task(tasks)
        elif choice == '6':
            filter_task(tasks)
        elif choice == '7':
            Search_task(tasks)
        elif choice == '8':
            edit_task(tasks)
        elif choice == '9':
            undo_task(tasks, trash)
        elif choice == '10':
            print("Exiting To-Do List. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()