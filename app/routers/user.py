from fastapi import APIRouter, Header, HTTPException, status
from models import (
    UserCreate,
    NightCreate,
    EventCreate,
    )
from persistence import (
    get_user as client_get_user,
    create_user as client_create_user,
    delete_user as client_delete_user,
    create_night as client_create_night,
    create_event as client_create_event
)
router = APIRouter(prefix="user")

@router.get('{user_id}/', status_code=status.HTTP_200_OK)
async def get_user(user_id: int, auth = Header()):
    user = await client_get_user(user_id,auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, auth = Header()):
    new_user = await client_create_user(user, auth)
    
    if not new_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"bad request")
    
@router.delete('{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, auth = Header()):
    
    success = await client_delete_user(user_id, auth)
    
    if success:
        return success
    else:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get('{user_id}/nights',status_code=status.HTTP_200_OK)
async def get_nights_per_user(user_id: int, auth = Header()):
    user = await client_get_user(user_id,auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

    nights = await get_nights_per_user(user_id, auth)
    
    if not nights:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return nights

@router.post('{user_id}/nights',status_code=status.HTTP_201_CREATED)
async def create_night(user_id: int,  new_night: NightCreate, auth = Header(),):
    user = await client_get_user(user_id,auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    return await client_create_night(
        new_night, auth
    )
    
@router.post('{user_id}/event', status_code=status.HTTP_201_CREATED)
async def create_event(user_id:int,event: EventCreate, auth = Header()):
    user = await client_get_user(user_id,auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    return await client_create_event(event, auth)
    
        
    



    