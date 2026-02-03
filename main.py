from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
from database import init_db

app = FastAPI(title="Chicken Road API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/")
def root():
    return {"status": "API Chicken Road online"}

app.include_router(router)
