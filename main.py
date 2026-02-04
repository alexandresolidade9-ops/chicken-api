from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from auth import router as auth_router
from database import init_db

app = FastAPI(title="Chicken Road API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # DEV
    allow_credentials=False,      # não use True com "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"status": "API Chicken Road online"}

# auth: /register, /login
app.include_router(auth_router)

# api: /signal
app.include_router(api_router)
