# Simple Task Manager (CLI)

A small command-line task manager written in Python.  
Tasks are stored in a local `tasks.json` file in the project directory.

## Features

- Add new tasks
- List all tasks or only pending ones
- Mark tasks as done
- Delete tasks
- Data persisted in JSON

## Usage

```bash
python app.py add "Buy milk"
python app.py add "Finish report"

python app.py list
python app.py list pending

python app.py done 1
python app.py delete 2
