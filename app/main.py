from fastapi import FastAPI
from .routers import sleep_router

from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()
app.include_router(sleep_router)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}