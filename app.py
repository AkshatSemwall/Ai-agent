from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="AI Agent System")

app.include_router(router)

@app.get("/")
def home():
    return {"status": "AI Agent System Running"}