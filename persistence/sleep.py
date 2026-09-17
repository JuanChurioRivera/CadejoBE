from services import (
    SupabaseClient,
    smooth_signal,
)
from models import (
    Sleep,
    SleepBase,
    SleepCreate,
    SleepSegment,
    SleepSegmentCreate,
    SleepSegmentBase,
    SleepEvent,
)
import numpy as np
from core.enums import Tables


async def get_sleep_from_night(night_id: int, sb_token: str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await (
            client.table(Tables.SLEEP)
            .select("*")
            .eq('night_id',night_id)
            .execute()
        )
        
        return Sleep.model_validate(res.data[0])
    except Exception:
        raise
    

    
async def create_sleep(sleep: SleepCreate, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await client.table(Tables.SLEEP).insert(sleep.model_dump_json()).execute()
        return SleepBase(**res.data[0])
    except Exception:
        raise
    
async def get_sleep_segments_from_sleep(sleep_id: int, sb_token: str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await (
            client.table(Tables.SLEEP_SEGMENT)
            .select("*")
            .eq('sleep_id',sleep_id)
            .execute()
        )
        
        return [SleepSegment.model_validate(row) for row in res.data]
    except Exception:
        raise
    
async def create_sleep_segments(s_segments: list[SleepSegmentCreate], sb_token: str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await (
            client.table(Tables.SLEEP_SEGMENT)
            .upsert([SleepSegmentCreate.model_validate(s_segement) for s_segement in s_segments])
            .execute()
        )
        return SleepSegmentBase(**res.data[0])
    except Exception:
        raise
    
async def process_sleep(sleep_events: list[SleepEvent]):
    
    print(f"sleep events: {sleep_events}")
    magnitude = [
        ((instant.x**2) + (instant.y**2) + (instant.z**2)) / 3
        for instant in sleep_events
    ]
    timestamps = [event.timestamp for event in sleep_events]
    
    print(f"magnitude: {magnitude}")
    
    smooth_signal(magnitude,timestamps)
    