from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.release.service import ReleaseService


def get_release_service() -> ReleaseService:
    return ReleaseService(SessionFactory)


ReleaseServiceDep = Annotated[ReleaseService, Depends(get_release_service)]
