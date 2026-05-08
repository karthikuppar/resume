from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api

app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0"
)

# --- Add this CORS section ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allows your Next.js app to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------

app.include_router(api.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the AI Resume Analyzer API"}