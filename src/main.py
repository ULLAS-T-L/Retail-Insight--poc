import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Retail Insights API",
    description="Backend for the Retail KPI Proof of Concept.",
    version="0.1.0"
)

# Connect all routes (from src/api/routes.py)
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Insights API. Make POST requests to /analyze"}

@app.get("/health")
def read_health():
    return {"status": "ok"}
