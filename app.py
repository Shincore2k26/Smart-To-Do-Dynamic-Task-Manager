from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks")
def get_tasks():
    return jsonify(load_tasks())

@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()
    data = request.json

    new_id = max([t["id"] for t in tasks], default=0) + 1

    task = {
        "id": new_id,
        "text": data["task"],
        "done": False
    }

    tasks.append(task)
    save_tasks(tasks)

    return jsonify(task)

@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"success": True})

@app.route("/toggle/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    tasks = load_tasks()
    updated = None

    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            updated = t

    save_tasks(tasks)
    return jsonify(updated)

if __name__ == "__main__":
    app.run(debug=True)