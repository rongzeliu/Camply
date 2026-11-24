from fastapi import FastAPI
from app.routers import camps, leaders, calendars, time_blocks

camply = FastAPI()
camply.include_router(camps.router)
camply.include_router(leaders.router)
camply.include_router(calendars.router)
camply.include_router(time_blocks.router)

@camply.get("/")
def read_root():
    return {"status": "ok"}


