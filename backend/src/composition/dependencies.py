from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.composition.service import CompositionService


def get_composition_service() -> CompositionService:
    return CompositionService(SessionFactory)


CompositionServiceDep = Annotated[CompositionService, Depends(get_composition_service)]
