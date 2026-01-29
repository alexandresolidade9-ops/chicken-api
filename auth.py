import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

from chicken_core import analyze_sequence

router = APIRouter()

USERS_FILE = "users.json"
signal_history = []


# ======================
# MODELS
# ======================
class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SignalRequest(BaseModel):
    history: List[float]


# ======================
# HELPERS
# ======================
def load_users():
    if not os.path.exists(USERS_FILE):
        return {"users": []}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"users": []}


def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ======================
# ROUTES
# ======================
@router.post("/register")
def register(req: RegisterRequest):
    data = load_users()

    if any(u["email"] == req.email for u in data["users"]):
        raise HTTPException(status_code=400, detail="Usuário já existe")

    data["users"].append({
        "email": req.email,
        "password": req.password
    })

    save_users(data)
    return {"status": "Usuário criado"}


@router.post("/login")
def login(req: LoginRequest):
    data = load_users()

    for user in data["users"]:
        if user["email"] == req.email and user["password"] == req.password:
            return {"status": "ok", "email": user["email"]}

    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@router.post("/signal")
def signal(req: SignalRequest):
    result = analyze_sequence(req.history)
    result["timestamp"] = datetime.utcnow().isoformat()
    signal_history.append(result)
    return result


@router.get("/history")
def history():
    return signal_history[-20:]
