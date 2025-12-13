from fastapi import FastAPI, File, UploadFile, Form
from typing import Optional

app = FastAPI()

@app.post("/scan")
async def scan(file: Optional[UploadFile] = File(None), text: Optional[str] = Form(None)):
    """
    This endpoint receives a file or text, and will eventually return a list of identified risks.
    For now, it returns a hardcoded success response.
    """
    return {
        "data": [
            {
                "risk": "The budget is tight",
                "category": "Financial",
                "context": "The project charter states that the budget is tight and that there is no room for error."
            },
            {
                "risk": "The deadline is aggressive",
                "category": "Schedule",
                "context": "The project plan shows an aggressive deadline that may not be achievable."
            }
        ]
    }

@app.get("/")
async def read_root():
    return {"Hello": "World"}
