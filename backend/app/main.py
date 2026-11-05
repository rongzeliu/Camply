from fastapi import FastAPI

camply = FastAPI()

@camply.get("/")
def read_root():
    return {"status": "ok"}