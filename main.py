from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

# Middleware CORS pour tests depuis le navigateur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Servir les fichiers statiques
if not os.path.exists("static"):
    os.mkdir("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Fichier de stockage
TASKS_FILE = "tasks.json"

# Modèle de tâche
class Task(BaseModel):
    id: int | None = None
    title: str
    completed: bool = False

# Routes
@app.get("/")
def read_root():
    return {"message": "FastAPI Task API is running!"}

@app.get("/tasks")
def list_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

@app.post("/tasks")
def add_task(task: Task):
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            tasks = json.load(f)
    task.id = len(tasks) + 1
    tasks.append(task.dict())
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)
    return task
