from fastapi import FastAPI, Depends, HTTPException
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

@camply.post("/camps", response_model=schemas.CampResponse)
def create_camps(camp: schemas.CampCreate, db : Session = Depends(get_db)):
    db_camp = models.Camp(name = camp.name, join_code = camp.join_code, start_date = camp.start_date, end_date = camp.end_date)
    db.add(db_camp)
    db.commit()
    db.refresh(db_camp)
    return db_camp

@camply.get("/camps/{camp_id}", response_model=schemas.CampResponse)
def get_camps(camp_id: int, db : Session = Depends(get_db)):
    camp = db.query(models.Camp).filter(models.Camp.id == camp_id).filter(models.Camp.deleted_at == None).first()
    if camp is None:
        raise HTTPException(status_code = 404, detail = "Camp not found")
    return camp