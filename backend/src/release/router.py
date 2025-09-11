from uuid import UUID
from fastapi import APIRouter
from src.release.schemas import ReleaseCreate, ReleaseUpdate, Release
from src.release.dependencies import ReleaseServiceDep
from src.schemas import SuccessResponse

router = APIRouter(prefix='/releases', tags=['release'])


@router.post('/', response_model=Release)
async def create_release(
    release_data: ReleaseCreate,
    service: ReleaseServiceDep
):
    return await service.create(release_data)


@router.get('/{release_id}', response_model=Release)
async def get_release(
    release_id: UUID,
    service: ReleaseServiceDep
):
    return await service.get(release_id)


@router.put('/{release_id}/update', response_model=Release)
async def update_release(
    release_id: UUID,
    release_data: ReleaseUpdate,
    service: ReleaseServiceDep
):
   
    return await service.update(release_id, release_data)


@router.delete('/{release_id}', response_model=SuccessResponse)
async def delete_release(
    release_id: UUID,
    service: ReleaseServiceDep
):
    await service.delete(release_id)
    return SuccessResponse(message='Release deleted')    
