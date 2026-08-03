from fastapi import APIRouter

router = APIRouter(prefix="user")

@router.get("/{user_id}")
async def user(user_id: int):
    return None