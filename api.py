from __future__ import annotations

from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel, Field

from chicken_core import analyze_sequence

router = APIRouter()


class SignalRequest(BaseModel):
    history: List[float] = Field(min_length=3)


@router.post("/signal")
def signal(req: SignalRequest) -> Dict[str, Any]:
    return analyze_sequence(req.history)


