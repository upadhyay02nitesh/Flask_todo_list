
from flask import Flask, redirect, render_template, request, jsonify, url_for
import mysql.connector

app = Flask(__name__)

# Database Connection Function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Rewa@1234",
            database="todo_db",
            autocommit=True
        )
        return conn
    except mysql.connector.Error as err:
        return {"error": f"Database connection failed: {err}"}, 500

# Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, due_date, status FROM tasks")
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        
        task_list = [{"id": t[0], "title": t[1], "description": t[2], "due_date": t[3], "status": t[4]} for t in tasks]
        return jsonify(task_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_particular_task(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, due_date, status FROM tasks where id=id")
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        
        task_list = [{"id": t[0], "title": t[1], "description": t[2], "due_date": t[3], "status": t[4]} for t in tasks]
        return jsonify(task_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create a new task
@app.route('/api/tasks', methods=['POST'])
def add_task():
    try:
        data = request.json
        required_fields = ["title", "description", "due_date"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO tasks (title, description, due_date, status) VALUES (%s, %s, %s, %s)"
        values = (data['title'], data['description'], data['due_date'], data.get('status', 'Pending'))
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Task added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an existing task
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        data = request.json
        required_fields = ["title", "description", "due_date", "status"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM tasks WHERE id=%s", (id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Task not found"}), 404

        sql = "UPDATE tasks SET title=%s, description=%s, due_date=%s, status=%s WHERE id=%s"
        values = (data['title'], data['description'], data['due_date'], data['status'], id)
        cursor.execute(sql, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"message": "Task updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Home Page - List Tasks
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, due_date, status FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add Task Page
@app.route('/add_task', methods=['GET', 'POST'])
def add_task_web():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form.get('status', 'Pending')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, due_date, status) VALUES (%s, %s, %s, %s)", 
                       (title, description, due_date, status))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('add_task.html')

# Update Task Page (Web)
@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task_web(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']

        cursor.execute("UPDATE tasks SET title=%s, description=%s, due_date=%s, status=%s WHERE id=%s", 
                       (title, description, due_date, status, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    
    # Fetch existing task data
    cursor.execute("SELECT id, title, description, due_date, status FROM tasks WHERE id=%s", (id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('update_task.html', task=task)

# Delete Task (Web)
@app.route('/delete_task/<int:id>')
def delete_task_web(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
