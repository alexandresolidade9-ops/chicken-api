import json
import os
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
from typing import List
from datetime import datetime

from chicken_core import analyze_sequence
from auth import hash_password   # 👈 ESTA LINHA

router = APIRouter()

# =====================
# CONFIG
# =====================
USERS_FILE = "users.json"
signal_history = []

# =====================
# MODELOS
# =====================
class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SignalRequest(BaseModel):
    history: List[float]

# =====================
# USUÁRIOS (LOGIN)
# =====================
def load_users():
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@router.post("/register")
def register(req: RegisterRequest):
    data = load_users()

    if any(u["email"] == req.email for u in data["users"]):
        raise HTTPException(status_code=400, detail="Usuário já existe")

    data["users"].append({
        "email": req.email,
        "password": hash_password(req.password)
    })

    save_users(data)
    return {"status": "Usuário criado com sucesso"}

@router.post("/login")
def login(req: LoginRequest):
    data = load_users()

    for user in data["users"]:
        if user["email"] == req.email and user["password"] == req.password:
            return {"status": "ok", "email": user["email"]}

    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# =====================
# SINAL
# =====================
@router.post("/signal")
def signal(req: SignalRequest):
    result = analyze_sequence(req.history)

    result["timestamp"] = datetime.utcnow().isoformat()
    signal_history.append(result)

    return result

@router.get("/history")
def history():
    return signal_history[-20:]
