from uuid import UUID
from fastapi import APIRouter
from src.auth.dependencies import OnlyAdminUserDep, CurrentUserDep
from src.record.schemas import RecordCreate, RecordUpdate, Record
from src.record.dependencies import RecordServiceDep
from src.schemas import SuccessResponse

router = APIRouter(prefix='/records', tags=['record'])


@router.post('/', response_model=Record)
async def create_record(
    record_data: RecordCreate,
    service: RecordServiceDep,
):
    return await service.create(record_data)


@router.get('/{record_id}', response_model=Record)
async def get_record(
    record_id: UUID,
    service: RecordServiceDep,
):
    return await service.get(record_id)


@router.get('/top-selling/last-year', response_model=list[Record])
async def get_top_selling_records_last_year(
    service: RecordServiceDep,
    limit: int = 10
):
    return await service.get_top_selling_records_last_year(limit)


@router.get('/top-selling/this-year', response_model=list[Record])
async def get_top_selling_records_this_year(
    service: RecordServiceDep,
    limit: int = 10
):
    return await service.get_top_selling_records_this_year(limit)


@router.put('/{record_id}/update', response_model=Record)
async def update_record(
    record_id: UUID,
    record_data: RecordUpdate,
    service: RecordServiceDep,
):
   
    return await service.update(record_id, record_data)


@router.delete('/{record_id}', response_model=SuccessResponse)
async def delete_record(
    record_id: UUID,
    service: RecordServiceDep,
):
    await service.delete(record_id)
    return SuccessResponse(message='Record deleted')    


@router.post('/{record_id}/performances/{performance_id}', response_model=SuccessResponse)
async def add_record_to_performance(
    record_id: UUID, 
    performance_id: UUID,
    service: RecordServiceDep,
):
    await service.add_record_to_performance(record_id, performance_id)
    return SuccessResponse(message='Record added to performance')    
