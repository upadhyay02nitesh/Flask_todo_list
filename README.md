Todo Management System

A simple Flask-based task management system with CRUD operations using MySQL.

Features

Add, update, delete, and view tasks

API endpoints for task management

Web interface for easy task handling

Uses MySQL for data storage

Installation

Clone the repository:

git clone <repo_url>

cd todo_list

Install dependencies:


Configure MySQL local  database in get_db_connection().

Run the application:

python app.py

API Endpoints

GET /api/tasks - Retrieve all tasks

POST /api/tasks - Add a new task

PUT /api/tasks/<id> - Update a task

DELETE /api/tasks/<id> - Delete a task

Error Handling

Returns proper status codes and messages for invalid requests.

Handles database connection errors gracefully.
