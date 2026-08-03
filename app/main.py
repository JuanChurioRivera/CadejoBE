from fastapi import FastAPI
from .routers import sleep_router
from supabase import create_client, Client
from dotenv import load_dotenv
from core import Credentials
import os
load_dotenv()

app = FastAPI()
app.include_router(sleep_router)
supabase: Client = create_client(supabase_url=os.getenv('host',""), supabase_key=os.getenv('key',""))
response = supabase.auth.sign_in_with_password(
    Credentials(
        email = 'juan.churio@hotmail.com',
        password='2Pacha$346'
    ).json
)


@app.get("/")
def read_root():
    return {response}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}