from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import hashlib
import sqlite3
from chicken_core import analyze_sequence

router = APIRouter()
DB = "database.db"

# ---------- MODELS ----------

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SignalRequest(BaseModel):
    history: List[float]

# ---------- HELPERS ----------

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- AUTH ----------

@router.post("/register")
def register(req: RegisterRequest):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (req.email, hash_password(req.password)),
        )
        db.commit()
        return {"status": "Usuário criado"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    finally:
        db.close()

@router.post("/login")
def login(req: LoginRequest):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE email = ?",
        (req.email,),
    )
    user = cursor.fetchone()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if hash_password(req.password) != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"status": "ok", "email": req.email}

# ---------- SIGNAL ----------

@router.post("/signal")
def signal(req: SignalRequest):
    return analyze_sequence(req.history)
