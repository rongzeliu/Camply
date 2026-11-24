from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.routers.calendars import get_valid_camp
from app.dependencies import get_db
from typing import List

def get_valid_calendar(calendar_id: int, camp: models.Camp = Depends(get_valid_camp), db: Session=Depends(get_db)) -> models.Calendar:
    calendar = db.query(models.Calendar).filter(models.Calendar.id == calendar_id).filter(models.Calendar.camp_id == camp.id).first()
    if calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return calendar

router = APIRouter(prefix="/camps/{camp_id}/calendars/{calendar_id}/time_blocks", tags=["time_blocks"], dependencies=[Depends(get_valid_calendar)])

@router.get("/", response_model=List[schemas.TimeBlockResponse])
def list_time_blocks(calendar_id: int, db: Session = Depends(get_db)):
    return db.query(models.TimeBlock).filter(models.TimeBlock.calendar_id == calendar_id).all()

@router.post("/", response_model=schemas.TimeBlockResponse)
def create_time_blocks(calendar_id: int, time_block: schemas.TimeBlockCreate, db: Session = Depends(get_db)):
    db_time_block = models.TimeBlock(calendar_id = calendar_id, 
                                    title = time_block.title,
                                    starts_at = time_block.starts_at,
                                    ends_at = time_block.ends_at,
                                    responsible_leader_id = time_block.responsible_leader_id,
                                    description = time_block.description
)
    try:
        db.add(db_time_block)
        db.commit()
        db.refresh(db_time_block)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 400, detail = "Bad Request")
    return db_time_block

@router.get("/{block_id}", response_model=schemas.TimeBlockResponse)
def get_time_block(block_id: int, calendar_id: int, db: Session = Depends(get_db)):
    time_block = db.query(models.TimeBlock).filter(models.TimeBlock.id == block_id).filter(models.TimeBlock.calendar_id == calendar_id).first()
    if time_block is None:
        raise HTTPException(status_code=404, detail="Time block not found")
    return time_block

@router.put("/{block_id}", response_model=schemas.TimeBlockResponse)
def put_time_blocks(block_id: int, calendar_id: int, time_block_update: schemas.TimeBlockUpdate, db: Session = Depends(get_db)):
    time_block = db.query(models.TimeBlock).filter(models.TimeBlock.id == block_id).filter(models.TimeBlock.calendar_id == calendar_id).first()
    if time_block is None:
        raise HTTPException(status_code = 404, detail = "Time block not found")
    update_data = time_block_update.model_dump(exclude_unset = True)
    for field, value in update_data.items():
        setattr(time_block, field, value)
    try:
        db.commit()
        db.refresh(time_block)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 400, detail = "Bad Request")
    return time_block