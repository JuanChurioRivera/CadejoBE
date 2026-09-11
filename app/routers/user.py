from fastapi import APIRouter, Header, HTTPException, status
from models import (
    UserCreate,
    NightCreate,
    EventCreate,
    NightEventCreate,
    )
from persistence import (
    get_user as client_get_user,
    create_user as client_create_user,
    delete_user as client_delete_user,
    create_night as client_create_night,
    create_event as client_create_event,
    get_night_from_user as client_get_night_from_user,
    get_events_from_user as client_get_events_from_user,
    associate_event_to_night as client_associate_event_to_night,
    get_events_from_night as client_get_events_from_night,
)
router = APIRouter(prefix="/user")

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, auth = Header()):
    new_user = await client_create_user(user, auth)
    
    if not new_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"bad request")
    
@router.delete('',status_code=status.HTTP_200_OK)
async def delete_user(auth = Header()):
    
    success = await client_delete_user(auth)
    
    if success:
        return success
    else:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get('/nights',status_code=status.HTTP_200_OK)
async def get_nights_per_user(auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

    nights = await client_get_night_from_user(auth)
    
    if not nights:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return nights

@router.post('/nights',status_code=status.HTTP_201_CREATED)
async def create_night(new_night: NightCreate, auth = Header(),):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    return await client_create_night(
        new_night, auth
    )
    
@router.post('/event', status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    return await client_create_event(event, auth)

@router.get('/event', status_code=status.HTTP_200_OK)
async def get_events(auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    events = await client_get_events_from_user(auth)
    
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return events

@router.post('/event/nights', status_code=status.HTTP_201_CREATED)
async def associate_event_to_night(night_event: NightEventCreate, auth = Header()):
    user = await client_get_user(auth)
    
    print("bro wtf")
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    return await client_associate_event_to_night(night_event, auth)

@router.get('/nights/{night_id}', status_code=status.HTTP_201_CREATED)
async def get_events_from_night(night_id: int, auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    events = await client_get_events_from_night(night_id, auth)
    
    return True
    
         
    



    