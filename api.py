from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext
from database import get_db
from chicken_core import analyze_sequence

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================= MODELS =================

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SignalRequest(BaseModel):
    history: List[float]

# ================= AUTH =================

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

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
    except:
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

    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"status": "ok", "email": req.email}

# ================= SIGNAL =================

@router.post("/signal")
def signal(req: SignalRequest):
    return analyze_sequence(req.history)
