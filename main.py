from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router

app = FastAPI(title="Chicken Road API")

# CORS (obrigatório para Flutter/Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API Chicken Road online"}

# ⬇️ REGISTRA AS ROTAS
app.include_router(api_router)


