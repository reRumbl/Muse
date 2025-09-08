from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.ensemble.service import EnsembleService


def get_ensemble_service() -> EnsembleService:
    return EnsembleService(SessionFactory)


EnsembleServiceDep = Annotated[EnsembleService, Depends(get_ensemble_service)]
