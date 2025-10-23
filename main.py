from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from jose import jwt
import json
import os

# Initialisation FastAPI
app = FastAPI()

# Middleware CORS pour tests depuis le navigateur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques (index.html)
if not os.path.exists("static"):
    os.mkdir("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Fichier de stockage et clé secrète JWT
TASKS_FILE = "tasks.json"
JWT_SECRET = "mehdim"

# Modèle de tâche
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False

# Route de test
@app.get("/")
def read_root():
    return {"message": "✅ FastAPI Task API is running!"}

# Login rapide
@app.post("/login")
def login(username: str = Query("demo")):
    token = jwt.encode({"username": username}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token}

# Lire toutes les tâches
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Ajouter une tâche
@app.post("/tasks", response_model=Task)
def add_task(task: Task):
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    task.id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append(task.dict())
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    return task

# Mettre à jour une tâche
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    if not os.path.exists(TASKS_FILE):
        raise HTTPException(status_code=404, detail="Task not found")
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = updated_task.title
            t["completed"] = updated_task.completed
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
            return t
    raise HTTPException(status_code=404, detail="Task not found")

# Supprimer une tâche
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if not os.path.exists(TASKS_FILE):
        raise HTTPException(status_code=404, detail="Task not found")
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)
    tasks = [t for t in tasks if t["id"] != task_id]
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    return {"message": "Task deleted"}