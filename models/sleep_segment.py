from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.enums.types import SleepStage


class SleepSegmentBase(BaseModel):
    idx: int | None = None
    sleep_stage: SleepStage | None = None
    starts_at: datetime
    ends_at: datetime
    duration: int | None = None


class SleepSegmentCreate(SleepSegmentBase):
    """Fields required to insert a new SleepSegment row."""
    sleep_id: int


class SleepSegment(SleepSegmentBase):
    """Full representation of public.SleepSegment.

    Note: sleep_id is the primary key (1:1 with Sleep), not an auto id.
    """
    model_config = ConfigDict(from_attributes=True)

    sleep_id: int
    created_at: datetime = Field(default_factory=datetime.now)