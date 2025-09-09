from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.musician.service import MusicianService


def get_musician_service() -> MusicianService:
    return MusicianService(SessionFactory)


MusicianServiceDep = Annotated[MusicianService, Depends(get_musician_service)]
