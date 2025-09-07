from uuid import UUID
from pydantic import BaseModel
from src.ensemble.models import EnsembleType


class EnsembleBase(BaseModel):
    name: str
    type: EnsembleType
    

class EnsembleCreate(EnsembleBase):
    pass


class EnsembleUpdate(BaseModel):
    name: str | None = None
    type: EnsembleType | None = None
    

class Ensemble(EnsembleBase):
    id: UUID
