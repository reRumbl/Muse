from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.record.service import RecordService


def get_record_service() -> RecordService:
    return RecordService(SessionFactory)


RecordServiceDep = Annotated[RecordService, Depends(get_record_service)]
