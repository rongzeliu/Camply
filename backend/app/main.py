from fastapi import FastAPI
from app.routers import camps, leaders, calendars

camply = FastAPI()
camply.include_router(camps.router)
camply.include_router(leaders.router)
camply.include_router(calendars.router)

@camply.get("/")
def read_root():
    return {"status": "ok"}


