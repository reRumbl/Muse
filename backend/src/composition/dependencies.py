from typing import Annotated
from fastapi import Depends
from src.dependencies import SessionDep
from src.composition.service import CompositionService


def get_composition_service(session: SessionDep) -> CompositionService:
    return CompositionService(session)


CompositionServiceDep = Annotated[CompositionService, Depends(get_composition_service)]
