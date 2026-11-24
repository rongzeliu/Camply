from pydantic import BaseModel, field_validator
from datetime import date, datetime

# Camp 
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
    

# Leader
class LeaderResponse(BaseModel):
    id: int 
    full_name: str
    
    model_config = {"from_attributes": True}
    
class LeaderCreate(BaseModel):
    full_name: str
    
    @field_validator("full_name")
    @classmethod
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("field must not be empty")
        return v.strip() 
    

# Calendar
class CalendarResponse(BaseModel):
    id: int 
    camp_id: int
    name: str
    
    model_config = {"from_attributes": True}
    
class CalendarCreate(BaseModel):
    name: str
    
    @field_validator("name")
    @classmethod
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("field must not be empty")
        return v.strip()
    

# Time Block
class TimeBlockResponse(BaseModel):
    id: int
    calendar_id: int 
    title: str 
    starts_at: datetime
    ends_at: datetime
    responsible_leader_id: int | None = None
    description: str | None = None 
    
    model_config = {"from_attributes": True}
    
class TimeBlockCreate(BaseModel):
    title: str 
    starts_at: datetime
    ends_at: datetime
    responsible_leader_id: int | None = None
    description: str | None = None 
    
    @field_validator("title")
    @classmethod
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("field must not be empty")
        return v.strip()

class TimeBlockUpdate(BaseModel):
    title: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    responsible_leader_id: int | None = None
    description: str | None = None
    
    @field_validator("title")
    @classmethod
    def must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("field must not be empty")
        return v.strip() if v else v
    
    