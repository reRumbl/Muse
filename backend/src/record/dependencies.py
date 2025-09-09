from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.record.service import RecordService, RecordReleaseService


def get_record_service() -> RecordService:
    return RecordService(SessionFactory)


RecordServiceDep = Annotated[RecordService, Depends(get_record_service)]


def get_record_release_service() -> RecordReleaseService:
    return RecordReleaseService(SessionFactory)


RecordReleaseServiceDep = Annotated[RecordReleaseService, Depends(get_record_release_service)]
