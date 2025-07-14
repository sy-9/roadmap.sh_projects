import json 
from tabulate import tabulate
from datetime import datetime
from typing import Generator

DATABASE_PATH = "task.json"

def load_database(path: str) -> dict: 
    try: 
        with open(path) as f: 
            database = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): 
        database = {}
    return database

def save_database(database, path):
    with open(path, "w") as f: 
        json.dump(database, f)
    
def add_task(database, description):
    today = datetime.today().isoformat()
    new_id = str(len(database) + 1)
    database[new_id] = {
        "description": description, 
        "status": "todo", 
        "created_at": today, 
        "updated_at": today
    }
    print(f"Added task {new_id}: {description}")
    list_task(database, status="all")

def update_task(database, id, description, status):
    database[id]["description"] = description
    database[id]["status"] = status
    updated_today = datetime.today().isoformat()
    database[id]["updated_at"] = updated_today
    list_task({id: database[id]})
    
def delete_task(database, id):
    list_task({id: database[id]})
    del database[id]

    new_database = {}
    keys = database.keys()
    for new_id, old_id in enumerate(keys, 1):
        new_database[new_id] = database[old_id]

    list_task(new_database)
    return new_database
    
def list_task(database: dict[str, dict], status = "all"): 
    valid_statuses = ["all", "todo", "in-progress", "done"]
                    
    if status not in valid_statuses: 
        print("Invalid status.")
        return #stop execution of this function
    
    if not database:
        print("Nothing to display.")
        return 

    table: Generator = (
        {
            "Id": id, 
            "Description": properties["description"],
            "Status": properties["status"], 
            "Created At": properties["created_at"],
            "Updated At": properties["updated_at"]
        }
        for id, properties in sorted(database.items())
        if status == "all" or properties["status"] == status
    )
    
    print(
        tabulate(table, headers="keys")
    )

def menu(): 
    db = load_database(DATABASE_PATH)

    print("==========================================================")
    print("TASK TRACKER")
    print("==========================================================")
    print("Current Task List: ")
    list_task(db)
    print("==========================================================")

    while True: 

        print("[1] Add Tasks")
        print("[2] Delete Tasks")
        print("[3] Update Task")
        print("[4] List Task")
        print("[5] Quit")
        choice = input("Which action do you want to perform? Choose 1-5.")  

        match choice: 
            #add
            case "1": 
                description = input("Enter task description: ")
                add_task(db, description)
            #delete
            case "2": 
                id = input("Enter task ID to delete: ").strip()
                delete_task(db, id)
            #update
            case "3": 
                id = int(input("Enter task ID to update: ").strip()) - 1
                description = input("Enter new description: ")
                status = input("Enter new status [todo/in-progress/done]: ").strip().lower()
                update_task(db, id, description, status)
            #list
            case "4": 
                status = input("Filter by status [all/todo/in-progress/done]: ").strip().lower()
                if status not in ["all", "todo", "in-progress", "done"]:
                    print("Invalid status.")
                    choice = input("Which action do you want to perform? Choose 1-5.") 
                else:
                    list_task(db, status)
            case "5": #quit
                    print("==========================================================")
                    print("DATA SAVED...")
                    print("==========================================================")
                    print("GOODBYE!")
                    save_database(db, DATABASE_PATH)
                    break
            case _: 
                    print("Please enter a valid input. ")
                    break
                    
def main(): 
    menu()
    
if __name__ == "__main__":
    main()
