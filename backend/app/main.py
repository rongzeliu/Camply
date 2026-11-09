from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import models, schemas
from typing import List

camply = FastAPI()

@camply.get("/")
def read_root():
    return {"status": "ok"}

@camply.get("/camps", response_model=List[schemas.CampResponse])
def get_camps(db : Session = Depends(get_db)):
    return db.query(models.Camp).filter(models.Camp.deleted_at == None).all()