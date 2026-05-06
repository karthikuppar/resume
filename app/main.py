from fastapi import FastAPI
from app.api.v1 import api

app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0"
)

app.include_router(api.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the AI Resume Analyzer API"}