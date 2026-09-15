from services import SupabaseClient
from models import (
    Sleep,
    SleepBase,
    SleepCreate,
    SleepSegment,
    SleepSegmentCreate,
    SleepSegmentBase
)

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
    