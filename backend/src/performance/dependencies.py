from typing import Annotated
from fastapi import Depends
from src.database import SessionFactory
from src.performance.service import PerformanceService


def get_performance_service() -> PerformanceService:
    return PerformanceService(SessionFactory)


PerformanceServiceDep = Annotated[PerformanceService, Depends(get_performance_service)]
