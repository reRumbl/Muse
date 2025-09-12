from typing import Annotated
from fastapi import Depends
from src.dependencies import SessionDep
from src.record.service import RecordService


def get_record_service(session: SessionDep) -> RecordService:
    return RecordService(session)


RecordServiceDep = Annotated[RecordService, Depends(get_record_service)]
