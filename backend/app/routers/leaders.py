from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.dependencies import get_db
from typing import List

router = APIRouter(prefix="/leaders", tags=["leaders"])

@router.get("/", response_model=List[schemas.LeaderResponse])
def list_leaders(db: Session = Depends(get_db)):
    return db.query(models.Leader).all()

@router.post("/", response_model=schemas.LeaderResponse)
def create_leader(leader: schemas.LeaderCreate, db: Session = Depends(get_db)):
    db_leader = models.Leader(full_name = leader.full_name)
    db.add(db_leader)
    db.commit()
    db.refresh(db_leader)
    return db_leader

@router.get("/{leader_id}", response_model=schemas.LeaderResponse)
def get_leader(leader_id: int, db: Session = Depends(get_db)):
    leader = db.query(models.Leader).filter(models.Leader.id == leader_id).first()
    if leader is None:
        raise HTTPException(status_code= 404, detail="leader not found")
    return leader