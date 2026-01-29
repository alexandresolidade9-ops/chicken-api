from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router  # 👈 AQUI ESTÁ A CORREÇÃO

app = FastAPI(title="Chicken Road API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API Chicken Road online"}

app.include_router(router)
