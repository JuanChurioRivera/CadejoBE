from datetime import datetime, date
from uuid import UUID
from .sleep import Sleep
from pydantic import BaseModel, ConfigDict, Field
 
 
class NightBase(BaseModel):
    user_id: UUID | None = None
 
 
class NightCreate(NightBase):
    """Fields required to insert a new Night row."""
    date: date 
 
 
class Night(NightBase):
    """Full representation of public.Night."""
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    date: date
    created_at: datetime = Field(default_factory=datetime.now)
    
    sleep: Sleep | None = None