import json
import sys
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(title):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "done": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Added task #{task['id']}: {task['title']}")


def list_tasks(show_done=True):
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return

    for t in tasks:
        if not show_done and t["done"]:
            continue
        status = "✅" if t["done"] else "⏳"
        print(f"{status} [{t['id']}] {t['title']} (created {t['created_at']})")


def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            if t["done"]:
                print(f"⚠️ Task #{task_id} is already done.")
            else:
                t["done"] = True
                save_tasks(tasks)
                print(f"✅ Marked task #{task_id} as done.")
            return
    print(f"❌ Task #{task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"❌ Task #{task_id} not found.")
        return

    # reassign IDs
    for index, t in enumerate(new_tasks, start=1):
        t["id"] = index

    save_tasks(new_tasks)
    print(f"🗑️ Deleted task #{task_id}.")


def print_help():
    help_text = """
Simple Task Manager (CLI)

Usage:
  python app.py add "Buy milk"
  python app.py list
  python app.py list pending
  python app.py done 2
  python app.py delete 3
  python app.py help
"""
    print(help_text.strip())


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("❌ Please provide a task title.")
            return
        title = " ".join(sys.argv[2:])
        add_task(title)

    elif command == "list":
        if len(sys.argv) >= 3 and sys.argv[2].lower() == "pending":
            list_tasks(show_done=False)
        else:
            list_tasks(show_done=True)

    elif command == "done":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("❌ Please provide a numeric task ID.")
            return
        mark_done(int(sys.argv[2]))

    elif command == "delete":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("❌ Please provide a numeric task ID.")
            return
        delete_task(int(sys.argv[2]))

    elif command == "help":
        print_help()

    else:
        print(f"❌ Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()
