from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.dependencies import get_db
from typing import List

def get_valid_camp(camp_id: int, db: Session = Depends(get_db)) -> models.Camp:
    camp = db.query(models.Camp).filter(models.Camp.id == camp_id, models.Camp.deleted_at.is_(None)).first()
    if camp is None:
        raise HTTPException(status_code=404, detail="Camp not found")
    return camp
    
router = APIRouter(prefix= "/camps/{camp_id}/calendars", tags=["calendars"], dependencies=[Depends(get_valid_camp)])

@router.get("/", response_model=List[schemas.CalendarResponse])
def list_calendars(camp_id: int, db: Session = Depends(get_db)):
    return db.query(models.Calendar).filter(models.Calendar.camp_id == camp_id).all()

@router.post("/", response_model=schemas.CalendarResponse)
def create_calendar(camp_id: int, calendar: schemas.CalendarCreate, db: Session = Depends(get_db)):
    db_calendar = models.Calendar(camp_id = camp_id, name = calendar.name)
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar

@router.get("/{calendar_id}", response_model=schemas.CalendarResponse)
def get_calendar(camp_id: int, calendar_id: int, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.camp_id == camp_id).filter(models.Calendar.id == calendar_id).first()
    if calendar is None:
        raise HTTPException(status_code= 404, detail="Calendar not found")
    return calendar