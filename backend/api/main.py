from fastapi import FastAPI
from .routers import scan

app = FastAPI()

app.include_router(scan.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RiskSkanner.ai API"}
