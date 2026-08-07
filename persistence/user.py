from services import SupabaseClient
from models import UserBase, User, UserCreate

from core.enums import Tables

async def get_user(id: int, sb_token: str) -> UserBase:
    client = await SupabaseClient().auth_client(sb_token)
    try:
        res =  await client.table(Tables.USER_PREFERENCES).select("*").eq("id",id).execute()
        return UserBase(**res)
    except Exception:
        raise
    
async def create_user(UserCreate: UserCreate, sb_token:str) -> UserBase:
    client = await SupabaseClient().auth_client(sb_token)
    try:
        res = await client.table(Tables.USER_PREFERENCES).insert(UserCreate.model_dump_json()).execute()
        return UserBase(**res)
    except Exception:
        raise
    
async def delete_user(user_id, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    try:
        res = await client.table(Tables.USER_PREFERENCES).delete().eq("id",user_id).execute()
        if res:
            return True
        else:
            return False
    except Exception:
        raise
