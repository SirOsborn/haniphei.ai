from pydantic import BaseModel
from typing import List

class RiskItem(BaseModel):
    risk: str
    category: str
    context: str

class ScanResult(BaseModel):
    data: List[RiskItem]
