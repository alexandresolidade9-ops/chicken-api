from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json, os
from chicken_core import analyze_sequence

router = APIRouter()

USERS_FILE = "users.json"

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SignalRequest(BaseModel):
    history: List[float]

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@router.post("/register")
def register(req: RegisterRequest):
    users = load_users()

    if any(u["email"] == req.email for u in users):
        raise HTTPException(status_code=400, detail="Usuário já existe")

    users.append({
        "email": req.email,
        "password": req.password
    })

    save_users(users)
    return {"status": "ok"}

@router.post("/login")
def login(req: LoginRequest):
    users = load_users()

    for u in users:
        if u["email"] == req.email and u["password"] == req.password:
            return {"status": "ok", "email": u["email"]}

    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.post("/signal")
def signal(req: SignalRequest):
    return analyze_sequence(req.history)
