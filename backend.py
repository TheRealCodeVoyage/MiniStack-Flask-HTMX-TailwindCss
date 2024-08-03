from flask import Flask, render_template, request

app = Flask(__name__)

tasks = []


@app.route("/")
def landing():
    return render_template('index.html', tasks=tasks)


@app.route("/add", methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    task_id = len(tasks) + 1
    task_completed = False
    if task_text:
        tasks.append({
            'task_id': task_id,
            'task_text': task_text,
            'task_completed': task_completed
        })
    component = f"""
    <li class="flex items-center space-x-2 p-2 bg-gray-100 rounded-md shadow-sm hover:bg-gray-200" id="task-{task_id}">
        <input type="checkbox" class="form-checkbox h-4 w-4 text-blue-600" hx-patch="/update-task/{ task_id }" { 'checked' if task_completed else '' }>
        <span class="text-gray-800">
            { task_text }
        </span>
        <button hx-delete="/delete/{ task_id }" hx-target="#task-{task_id}" hx-confirm="Are you sure you want to delete this task?" hx-swap="outerHTML swap:1s" class="text-red-600 hover:text-red-800">
        Delete
        </button>
    </li>
    """
    return component


@app.route("/update-task/<int:task_id>", methods=['PATCH'])
def update_task(task_id):
    for task in tasks:
        if task['task_id'] == task_id:
            task['task_completed'] = not task['task_completed']
            break
    return '', 204  # No Content response


@app.route("/delete/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['task_id'] != task_id]
    print(tasks)
    return "", 200  # No content response
