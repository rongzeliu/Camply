from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app import models, schemas
from app.dependencies import get_db
from typing import List

router = APIRouter(prefix="/camps", tags=["camps"])

@router.get("/", response_model=List[schemas.CampResponse])
def list_camps(db : Session = Depends(get_db)):
    return db.query(models.Camp).filter(models.Camp.deleted_at == None).all()

@router.post("/", response_model=schemas.CampResponse)
def create_camps(camp: schemas.CampCreate, db : Session = Depends(get_db)):
    db_camp = models.Camp(name = camp.name, join_code = camp.join_code, start_date = camp.start_date, end_date = camp.end_date)
    db.add(db_camp)
    db.commit()
    db.refresh(db_camp)
    return db_camp

@router.get("/{camp_id}", response_model=schemas.CampResponse)
def get_camp(camp_id: int, db : Session = Depends(get_db)):
    camp = db.query(models.Camp).filter(models.Camp.id == camp_id).filter(models.Camp.deleted_at == None).first()
    if camp is None:
        raise HTTPException(status_code = 404, detail = "Camp not found")
    return camp

@router.put("/{camp_id}", response_model=schemas.CampResponse)
def put_camps(camp_id: int, camp_update: schemas.CampUpdate, db: Session = Depends(get_db)):
    camp = db.query(models.Camp).filter(models.Camp.id == camp_id).filter(models.Camp.deleted_at == None).first()
    if camp is None:
        raise HTTPException(status_code = 404, detail = "Camp not found")
    update_data = camp_update.model_dump(exclude_unset = True)
    for field, value in update_data.items():
        setattr(camp, field, value)
    try:
        db.commit()
        db.refresh(camp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409, detail = "Camp with join code that already exists")
    return camp

@router.delete("/{camp_id}")
def delete_camps(camp_id: int, db: Session = Depends(get_db)):
    camp = db.query(models.Camp).filter(models.Camp.id == camp_id).filter(models.Camp.deleted_at == None).first()
    if camp is None:
        raise HTTPException(status_code = 404, detail = "Camp not found")
    camp.deleted_at = datetime.now()
    db.commit()
    return {"message" : "Camp moved to trash"}