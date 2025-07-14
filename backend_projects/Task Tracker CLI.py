import json 
import tabulate
from datetime import datetime
from typing import Generator

DATABASE_PATH = "task.json"

def load_database(path: str) -> dict: 
    try: 
        with open(path, "r") as f: 
            database = json.load(f)
    except FileNotFoundError: 
        database = {}
    return database

def save_database(database, path):
    with open(path, "w") as f: 
        json.dumps(database, f)
    
def add_task(database, description):
    today = datetime.today().isoformat()
    new_id = str(len(database))
    database[new_id] = {
        "description": description, 
        "status": "todo", 
        "created_at": today, 
        "updated_at:": today
    }
    print(f"Added task {new_id}: {description}")
    list_task({id: database[id]})

def update_task(database, id, description, status):
    database[id]["description"] = description
    database[id]["status"] = status
    updated_today = datetime.today().isoformat()
    database[id]["updated_at"] = updated_today
    list_task({id: database[id]})
    
def delete_task(database, id):
    list_task({id: database[id]})
    del database[id]

    # change index
    
def list_task(database: dict[str, dict], status = ["todo", "in-progress", "done"]): 
    table: Generator = (
        {
            "Id": id, 
            "Description": properties["description"],
            "Status": properties["status"], 
            "Created At": properties["created_at"],
            "Updated At": properties["updated_at"]
        }
        for id, properties in sorted(database.items())
    )
    
    print(
        tabulate(table, headers="keys") or "Nothing to display"
    )

def console(): 
    db = load_database
     
    while True: 
        print("==========================================================")
        print("TASK TRACKER")
        print("==========================================================")
        print("Current Task List: ")
        load_database(DATABASE_PATH)
        print("==========================================================")
        print("[1] Add Tasks")
        print("[2] Delete Tasks")
        print("[3] Update Task")
        print("[4] List Task")
        print("[5] Quit")
        choice = input("Which action do you want to perform? Choose 1 -5.") 

        match choice: 
            case 1: 
                description = input("Enter task description: ")
                add_task(db, description)
            case 2:
                id = input("Enter task ID to delete: ").strip()
                delete_task(db, id)
            case 3: 
                id = input("Enter task ID to update: ").strip()
                description = input("Enter new description: ")
                status = input("Enter new status [todo/in-progress/done]: ").strip().lower()
                update_task(db, id, description, status)
            case 4: 
                status = input("Filter by status [all/todo/in-progress/done]: ").strip().lower()
                if status not in ["all", "todo", "in-progress", "done"]:
                    print("Invalid status.")
                else:
                    list_task(db, status)
            case 5: 
                    save_database(DATABASE_PATH, db)
                    exit("GOODBYE!")
            case _: 
                    print("Please enter a valid input. ")

def main(): 
    console()
    
if __name__ == "__main__":
    main()