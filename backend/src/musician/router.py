from uuid import UUID
from fastapi import APIRouter
from src.auth.dependencies import OnlyAdminUserDep, CurrentUserDep
from src.musician.schemas import MusicianCreate, MusicianUpdate, Musician
from src.musician.dependencies import MusicianServiceDep
from src.schemas import SuccessResponse

router = APIRouter(prefix='/musicians', tags=['musician'])


@router.post('/', response_model=Musician)
async def create_musician(
    musician_data: MusicianCreate,
    service: MusicianServiceDep,
    user: OnlyAdminUserDep
):
    return await service.create(musician_data)


@router.get('/{musician_id}', response_model=Musician)
async def get_musician(
    musician_id: UUID,
    service: MusicianServiceDep,
    user: CurrentUserDep
):
    return await service.get(musician_id)


@router.put('/{musician_id}/update', response_model=Musician)
async def update_musician(
    musician_id: UUID,
    musician_data: MusicianUpdate,
    service: MusicianServiceDep,
    user: OnlyAdminUserDep
):
   
    return await service.update(musician_id, musician_data)


@router.delete('/{musician_id}', response_model=SuccessResponse)
async def delete_musician(
    musician_id: UUID,
    service: MusicianServiceDep,
    user: OnlyAdminUserDep
):
    await service.delete(musician_id)
    return SuccessResponse(message='Musician deleted')    
