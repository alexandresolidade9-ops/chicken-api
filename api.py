from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from chicken_core import analyze_sequence

app = FastAPI(title="Chicken Road Signal API")

# 🔓 LIBERAR CORS (IMPORTANTE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção muda isso
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SignalRequest(BaseModel):
    history: List[float]

@app.post("/signal")
def signal(req: SignalRequest):
    return analyze_sequence(req.history)
