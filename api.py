from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from chicken_core import analyze_sequence

router = APIRouter()

class SignalRequest(BaseModel):
    history: List[float]

@router.post("/signal")
def signal(req: SignalRequest):
    return analyze_sequence(req.history)

