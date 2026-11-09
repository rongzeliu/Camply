from pydantic import BaseModel
from datetime import date

class CampResponse(BaseModel):
    id: int 
    name: str 
    join_code: str
    start_date: date
    end_date: date
    
    model_config = {"from_attributes": True}
    
class CampCreate(BaseModel):
    name: str
    join_code: str
    start_date: date
    end_date: date
    
    model_config = {"from_attributes": True}