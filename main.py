from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import json
import os

# --- Initialize FastAPI ---
app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve static files ---
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Data storage ---
TASKS_FILE = "tasks.json"
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        json.dump([], f)

# --- Task model ---
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False

# --- Routes ---
@app.get("/")
def read_root():
    return {"message": "FastAPI Task API is running!"}

@app.get("/tasks")
def get_tasks():
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
    task.id = (tasks[-1]["id"] + 1) if tasks else 1
    tasks.append(task.dict())
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
    return task
