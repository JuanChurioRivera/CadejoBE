from fastapi import APIRouter, Header, HTTPException, status
from models import (
    UserCreate,
    NightCreate,
    EventCreate,
    NightEventCreate,
    SleepEvent,
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
    get_sleep_from_night as client_get_sleep_from_night,
    get_sleep_segments_from_sleep as client_get_sleep_segments_from_sleep,
    process_sleep
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
    
@router.post('/events', status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    return await client_create_event(event, auth)

@router.get('/events', status_code=status.HTTP_200_OK)
async def get_events(auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    events = await client_get_events_from_user(auth)
    
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return events

@router.post('/nights/{night_id}/events', status_code=status.HTTP_201_CREATED)
async def associate_event_to_night(night_id: int, night_event: NightEventCreate, auth = Header()):
    user = await client_get_user(auth)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    night_event.night_id = night_id
    
    return await client_associate_event_to_night(night_event, auth)

@router.get('/nights/{night_id}/events', status_code=status.HTTP_200_OK)
async def get_events_from_night(night_id: int, auth = Header()):
     
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    return await client_get_events_from_night(night_id, auth)

@router.get('/nights/{night_id}/sleep', status_code=status.HTTP_200_OK)
async def get_sleep_from_night(night_id: int, auth = Header()):
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    sleep = await client_get_sleep_from_night(night_id, auth)
    s_segments = await client_get_sleep_segments_from_sleep(sleep.id, auth)
    sleep.sleep_segments = s_segments
    
    if not sleep:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "sleep not found")
    
    return sleep

@router.post('/nights/{night_id}/sleep', status_code=status.HTTP_201_CREATED)
async def record_sleep(night_id: int, sleep_events: list[SleepEvent] ,auth = Header()):
    
    user = await client_get_user(auth)
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    
    await process_sleep(sleep_events)
    
    return status.HTTP_200_OK
    