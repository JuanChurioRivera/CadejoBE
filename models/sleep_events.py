from pydantic import BaseModel
from datetime import date, datetime

class SleepEvent(BaseModel):
    idx: int
    x: float
    y: float
    z: float
    timestamp: datetime