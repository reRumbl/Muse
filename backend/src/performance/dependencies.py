from typing import Annotated
from fastapi import Depends
from src.dependencies import SessionDep
from src.performance.service import PerformanceService


def get_performance_service(session: SessionDep) -> PerformanceService:
    return PerformanceService(session)


PerformanceServiceDep = Annotated[PerformanceService, Depends(get_performance_service)]
