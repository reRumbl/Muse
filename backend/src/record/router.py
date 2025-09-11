from uuid import UUID
from fastapi import APIRouter
from src.record.schemas import RecordCreate, RecordUpdate, Record
from src.record.dependencies import RecordServiceDep
from src.schemas import SuccessResponse

router = APIRouter(prefix='/records', tags=['record'])


@router.post('/', response_model=Record)
async def create_record(
    record_data: RecordCreate,
    service: RecordServiceDep
):
    return await service.create(record_data)


@router.get('/{record_id}', response_model=Record)
async def get_record(
    record_id: UUID,
    service: RecordServiceDep
):
    return await service.get(record_id)


@router.put('/{record_id}/update', response_model=Record)
async def update_record(
    record_id: UUID,
    record_data: RecordUpdate,
    service: RecordServiceDep
):
   
    return await service.update(record_id, record_data)


@router.delete('/{record_id}', response_model=SuccessResponse)
async def delete_record(
    record_id: UUID,
    service: RecordServiceDep
):
    await service.delete(record_id)
    return SuccessResponse(message='Record deleted')    


@router.post('/{record_id}/performances/{performance_id}', response_model=SuccessResponse)
async def add_record_to_performance(
    record_id: UUID, 
    performance_id: UUID,
    service: RecordServiceDep
):
    await service.add_record_to_performance(record_id, performance_id)
    return SuccessResponse(message='Record added to performance')    
