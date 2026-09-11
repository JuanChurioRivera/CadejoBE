from services import SupabaseClient
from models import UserBase, User, UserCreate
import jwt
from core.enums import Tables

async def get_user(id: int, sb_token: str) -> UserBase:
    client = await SupabaseClient().auth_client(sb_token)
    try:
        res =  await (
            client.table(Tables.USER_PREFERENCES)
            .select("*")
            .eq("user_id",id)
            .execute()
            )
        return User(**res.data[0])
    except Exception:
        raise
    
async def create_user(user_create: UserCreate, sb_token: str) -> UserBase:
    client = await SupabaseClient().auth_client(sb_token)
    
    print(f"client: {client.auth}")
    
    payload = jwt.decode(
        sb_token,
        options={"verify_signature": False},
    )
    user_id = payload["sub"]

    user = User(
        **user_create.model_dump(exclude={"user_id"}),
        user_id=user_id,
    )
    
    try:
        res = await (
            client.table(Tables.USER_PREFERENCES)
            .insert(user.model_dump(mode="json"))
            .execute()
        )
    except Exception as e:
        print("Supabase insert failed:", repr(e))
        raise

    if not res.data:
        raise RuntimeError("User was inserted but Supabase returned no data")

    return UserBase.model_validate(res.data[0])
    
async def delete_user(user_id, sb_token:str):
    client = await SupabaseClient().auth_client(sb_token)
    try:
        res = await (
            client.table(Tables.USER_PREFERENCES)
            .delete()
            .eq('user_id',user_id)
            .execute()
        )
        if res:
            return True
        else:
            return False
    except Exception: 
        raise
