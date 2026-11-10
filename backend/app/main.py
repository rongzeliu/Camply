from fastapi import FastAPI
from app.routers import camps

camply = FastAPI()
camply.include_router(camps.router)

@camply.get("/")
def read_root():
    return {"status": "ok"}


    
