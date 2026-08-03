from datetime import datetime
 
from pydantic import BaseModel, ConfigDict, Field
 
 
class EventBase(BaseModel):
    custom: bool | None = False
    name: str | None = None
    description: str | None = None
 
 
class EventCreate(EventBase):
    """Fields required to insert a new Event row."""
    custom: bool
    name: str
    description: str | None = None
 
 
class Event(EventBase):
    """Full representation of public.Event."""
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    created_at: datetime = Field(default_factory=datetime.now)