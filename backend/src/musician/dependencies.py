from typing import Annotated
from fastapi import Depends
from src.dependencies import SessionDep
from src.musician.service import MusicianService


def get_musician_service(session: SessionDep) -> MusicianService:
    return MusicianService(session)


MusicianServiceDep = Annotated[MusicianService, Depends(get_musician_service)]
