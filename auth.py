from __future__ import annotations

import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext

from database import fetchone, execute

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


@router.post("/register")
def register(req: RegisterRequest):
    try:
        execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (req.email, _hash_password(req.password)),
        )
        return {"status": "ok"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Usuário já existe")


@router.post("/login")
def login(req: LoginRequest):
    row = fetchone("SELECT email, password FROM users WHERE email = ?", (req.email,))
    if row is None:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not _verify_password(req.password, row["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"status": "ok", "email": row["email"]}

