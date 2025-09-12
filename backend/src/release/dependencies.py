from typing import Annotated
from fastapi import Depends
from src.dependencies import SessionDep
from src.release.service import ReleaseService


def get_release_service(session: SessionDep) -> ReleaseService:
    return ReleaseService(session)


ReleaseServiceDep = Annotated[ReleaseService, Depends(get_release_service)]
