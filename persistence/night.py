from services import SupabaseClient, get_user_id_from_token
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

async def get_night_from_user(sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await (
            client.table(Tables.NIGHT)
            .select("*")
            .eq('user_id',get_user_id_from_token(sb_token))
            .execute()
        )
        nights = [Night.model_validate(row) for row in res.data]
        return nights
    except Exception:
        raise
    
async def create_night(night: NightCreate, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    night.user_id = get_user_id_from_token(sb_token)
    try:
        res = await (
            client.table(Tables.NIGHT)
            .insert(night.model_dump(mode="json"))
            .execute()
        )
        return Night.model_validate(res.data[0])
    except Exception:
        raise
    
async def create_event(event: EventCreate, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    event.by_user_id = get_user_id_from_token(sb_token)
    
    try:
        res = await (
            client.table(Tables.EVENT)
            .insert(event.model_dump(mode="json"))
            .execute()
        )
        return Event.model_validate(res.data[0])
    except Exception:
        raise
    
async def get_events_from_user(sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        events = await (
            client.table(Tables.EVENT)
            .select("*")
            .eq('by_user_id',get_user_id_from_token(sb_token))
            .eq('custom',False)
            .execute()
        ) 
    
        return [Event.model_validate(row) for row in events.data]

    except Exception:
        raise
    
async def associate_event_to_night(night_event: NightEventCreate, sb_token: str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        events = await (
            client.table(Tables.EVENT)
            .select("*")
            .eq('by_user_id',get_user_id_from_token(sb_token))
            .eq('custom',False)
            .execute()
        )
        
        possible_events = [Event.model_validate(row).id for row in events.data] 
        
        if night_event.event_id not in possible_events:
            raise RuntimeError("Event does not belong to user")
        
        night = await (
            client.table(Tables.NIGHT)
            .select("*")
            .eq('user_id',get_user_id_from_token(sb_token))
            .execute()
        )
        
        if night_event.night_id != Night(**night.data[0]).id:
            raise RuntimeError("Night does not belong to user")
            
        res = await (
            client.table(Tables.NIGHT_EVENT)
            .insert(night_event.model_dump(mode="json"))
            .execute()
        )
        
        return NightEvent(**res.data[0])
    except Exception:
        raise
    
async def get_events_from_night(night_id: int, sb_token: str):
    client = await SupabaseClient().auth_client(sb_token)
    
    try:
        res = await (
            client.table(Tables.NIGHT_EVENT)
            .select(f"*, {Tables.EVENT}(*)")
            .eq('night_id',night_id)
            .execute()
        )
        
        print(f"res.data: {res.data}")
        
        return True
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
        
        return NightEvent(**res.data[0])
    except Exception:
        raise