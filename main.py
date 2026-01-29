from fastapi import FastAPI
from api import router as api_router

app = FastAPI(title="Chicken Road API")

@app.get("/")
def root():
    return {"status": "API Chicken Road online"}

app.include_router(api_router)
