import json
import os
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

router = APIRouter()
USERS_FILE = "users.json"


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


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
    data = load_users()

    if any(u["email"] == req.email for u in data["users"]):
        raise HTTPException(status_code=400, detail="Usuário já existe")

    data["users"].append({
        "email": req.email,
        "password": hash_password(req.password)
    })

    save_users(data)
    return {"status": "Usuário criado"}


@router.post("/login")
def login(req: LoginRequest):
    data = load_users()

    for user in data["users"]:
        if user["email"] == req.email and verify_password(
            req.password,
            user["password"]
        ):
            return {"status": "ok", "email": user["email"]}

    raise HTTPException(status_code=401, detail="Credenciais inválidas")


