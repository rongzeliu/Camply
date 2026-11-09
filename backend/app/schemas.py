from pydantic import BaseModel, field_validator
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
    
    @field_validator("name", "join_code")
    @classmethod
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("field must not be empty")
        return v.strip()

class CampUpdate(BaseModel):
    name: str | None = None
    join_code: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    
    @field_validator("name", "join_code")
    @classmethod
    def must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("field must not be empty")
        return v.strip() if v else v