from uuid import UUID
from fastapi import APIRouter
from src.performance.schemas import PerformanceCreate, PerformanceUpdate, Performance
from src.performance.dependencies import PerformanceServiceDep
from src.schemas import SuccessResponse

router = APIRouter(prefix='/performances', tags=['performance'])


@router.post('/', response_model=Performance)
async def create_performance(
    performance_data: PerformanceCreate,
    service: PerformanceServiceDep
):
    return await service.create(performance_data)


@router.get('/{performance_id}', response_model=Performance)
async def get_performance(
    performance_id: UUID,
    service: PerformanceServiceDep
):
    return await service.get(performance_id)


@router.put('/{performance_id}/update', response_model=Performance)
async def update_performance(
    performance_id: UUID,
    performance_data: PerformanceUpdate,
    service: PerformanceServiceDep
):
   
    return await service.update(performance_id, performance_data)


@router.delete('/{performance_id}', response_model=SuccessResponse)
async def delete_performance(
    performance_id: UUID,
    service: PerformanceServiceDep
):
    await service.delete(performance_id)
    return SuccessResponse(message='Performance deleted')    
