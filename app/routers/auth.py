from fastapi import APIRouter
from core import Credentials
from ...config import config

router = APIRouter(prefix="auth")

@router.post("/")
async def sign_in(credentials: Credentials):
    pass