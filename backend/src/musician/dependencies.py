from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.musician.service import MusicianService


def get_musician_service() -> MusicianService:
    return MusicianService(SessionFactory)


EnsembleServiceDep = Annotated[MusicianService, Depends(get_musician_service)]
