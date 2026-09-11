from supabase import create_async_client, Client
from dotenv import load_dotenv
from config import config
from dataclasses import dataclass
from jwt import decode
@dataclass
class SupabaseClient:
    host = config.supabase_host
    key = config.supabase_key
    
    async def client(self):

        return await create_async_client(
            supabase_url=self.host,
            supabase_key=self.key,
        )
    
    async def auth_client(self, token: str):
        client = await self.client()
        client.postgrest.auth(token)
        return client 
    
def get_user_id_from_token(token: str) -> str:
    payload = decode(
        token,
        options={"verify_signature": False},
    )
    return payload["sub"]      
        