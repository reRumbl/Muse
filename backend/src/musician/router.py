from uuid import UUID
from fastapi import APIRouter
from src.musician.schemas import MusicianCreate, MusicianUpdate, Musician
from src.musician.dependencies import MusicianServiceDep

router = APIRouter(prefix='/musicians', tags=['musician'])


@router.post('/')
async def create_musician(
    musician_data: MusicianCreate,
    service: MusicianServiceDep
):
    return await service.create(musician_data)


@router.get('/{musician_id}')
async def get_musician(
    musician_id: UUID,
    service: MusicianServiceDep
):
    return await service.get(musician_id)


@router.put('/{musician_id}/update')
async def update_musician(
    musician_id: UUID,
    musician_data: MusicianUpdate,
    service: MusicianServiceDep
):
   
    return await service.update(musician_id, musician_data)

@router.delete('/{musician_id}')
async def delete_musician(
    musician_id: UUID,
    service: MusicianServiceDep
):
    return await service.delete(musician_id)
    
