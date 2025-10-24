FastAPI Task API Demo

Demo project of a simple task management API using FastAPI and Python.

🔹 Description

This application is a basic API that allows you to create, list, update, and delete tasks.
It demonstrates:
	•	Using FastAPI for building REST endpoints
	•	Handling JSON data stored in tasks.json
	•	Simple JWT-based authentication
	•	Minimal frontend to test endpoints via a web browser

🔹 Features
	•	Add a task (POST /tasks)
	•	List all tasks (GET /tasks)
	•	Update a task (PUT /tasks/{id})
	•	Delete a task (DELETE /tasks/{id})
	•	Simple authentication via POST /login

🔹 Tech Stack
	•	Python 3.11
	•	FastAPI
	•	Uvicorn
	•	Python-JOSE (JWT)
	•	HTML/JavaScript for minimal frontend

  🔹 How to Run
  
	1.	Clone the repository:
  git clone git@github.com:MehdiMaadadi/Fast-task-api-demo.git
cd Fast-task-api-demo

2.	Install dependencies:
python3 -m pip install -r requirements.txt


3.	Start the server:
uvicorn main:app --reload --port 8000

4.	Open the minimal frontend (optional) in a browser:
static/index.html


🔹 Example Requests : 
    # List tasks
curl https://fast-task-api-demo-3.onrender.com/static/index.html

# Add a task
curl -X POST "https://fast-task-api-demo-3.onrender.com/static/index.html\
     -H "Content-Type: application/json" \
     -d '{"title":"My first task","completed":false}'

🔹 About

This project is designed to showcase my Backend development skills (Python/FastAPI) and serves as a portfolio example.


