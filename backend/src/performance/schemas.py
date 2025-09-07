from uuid import UUID
from pydantic import BaseModel


class PerformanceBase(BaseModel):
    composition_id: UUID
    ensemble_id: UUID


class PerformanceCreate(PerformanceBase):
    pass


class PerformanceUpdate(BaseModel):
    composition_id: UUID | None = None
    ensemble_id: UUID | None = None


class Performance(PerformanceBase):
    id: UUID
