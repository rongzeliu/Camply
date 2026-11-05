from fastapi import FastAPI
from app.database import engine, Base

camply = FastAPI()

@camply.get("/")
def read_root():
    return {"status": "ok"}