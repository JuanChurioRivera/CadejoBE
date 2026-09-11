from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field

from core.enums.types import UserRole

class UserBase(BaseModel):
    email: str 
    name: str | None = None
    dob: date | None = None
    role: UserRole | None = None
    nocturne: bool | None = None
    


class UserCreate(UserBase):
    """Fields required to insert a new UserPreferences row."""
    role : UserRole


class User(UserBase):
    """Full representation of public.UserPreferences."""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: str
    updated_at: datetime | None = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)