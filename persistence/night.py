from services import SupabaseClient
from models import (
    Night,
    NightBase,
    NightCreate,
    NightEvent,
    NightEventBase,
    NightEventCreate,
    Event,
    EventCreate,
    EventBase
)

from core.enums import Tables

async def get_night_from_user(user_id: int, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await (
            client.table(Tables.NIGHT)
            .select(f"*,{Tables.SLEEP}(*)")
            .eq('user_id',user_id)
            .execute()
        )
        nights = [Night.model_validate(row) for row in res.data]
        return nights
    except Exception:
        raise
    
async def create_night(night: NightCreate, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await client.table(Tables.NIGHT).insert(night.model_dump_json()).execute()
        return NightBase(**res)
    except Exception:
        raise
    
async def create_event(event: EventCreate, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)

    try:
        res = await (
            client.table(Tables.EVENT)
            .insert(event)
            .execute()
        )
        return EventBase(**res)
    except Exception:
        raise
    
async def create_event_night(night_event: NightEventCreate, sb_token: str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await (
            client.table(Tables.NIGHT_EVENT)
            .insert(night_event.model_dump_json())
            .execute()
        )
    except Exception:
        raise