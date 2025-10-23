from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI Task API is running!"}




Simplify main.py for Render deployment
