from uuid import UUID
from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
