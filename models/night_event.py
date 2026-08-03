from datetime import datetime
 
from pydantic import BaseModel, ConfigDict
 
 
class NightEventBase(BaseModel):
    night_id: int
    event_id: int | None = None
    time: datetime | None = None  # naive datetime (timestamp without time zone)
 
 
class NightEventCreate(NightEventBase):
    """Fields required to insert a new NightEvent   row."""
    night_id: int
    eventid: int
 
 
class NightEvent(NightEventBase):
    """Full representation of public.NightEvent."""
    model_config = ConfigDict(from_attributes=True)
 
    id: int