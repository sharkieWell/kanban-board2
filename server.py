from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='.')
CORS(app)

def init_db():
    conn = sqlite3.connect('kanban.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks
        (id TEXT PRIMARY KEY,
         title TEXT NOT NULL,
         priority TEXT NOT NULL,
         status TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('kanban.db')
    c = conn.cursor()
    c.execute('SELECT id, title, priority, status FROM tasks')
    tasks = [{'id': row[0], 'title': row[1], 'priority': row[2], 'status': row[3]} 
             for row in c.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json
    conn = sqlite3.connect('kanban.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (id, title, priority, status) VALUES (?, ?, ?, ?)',
              (task['id'], task['title'], task['priority'], task['status']))
    conn.commit()
    conn.close()
    return jsonify(task)

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = request.json
    conn = sqlite3.connect('kanban.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ? WHERE id = ?',
              (task['status'], task_id))
    conn.commit()
    conn.close()
    return jsonify(task)

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 