from typing import Annotated
from fastapi import Depends
from src.dependencies import SessionDep
from src.ensemble.service import EnsembleService


def get_ensemble_service(session: SessionDep) -> EnsembleService:
    return EnsembleService(session)


EnsembleServiceDep = Annotated[EnsembleService, Depends(get_ensemble_service)]
