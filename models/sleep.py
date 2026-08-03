from datetime import datetime
 
from pydantic import BaseModel, ConfigDict, Field
 
from core.enums.types import QualityOfSleep
 
 
class SleepBase(BaseModel):
    night_id: int | None = None
    duration: int | None = None
    PSQI: int | None = 0
    quality_of_sleep: QualityOfSleep | None = None
 
 
class SleepCreate(SleepBase):
    """Fields required to insert a new Sleep row."""
    night_id: int
    duration: int
    pass
 
 
class Sleep(SleepBase):
    """Full representation of public.Sleep."""
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    created_at: datetime = Field(default_factory=datetime.now)