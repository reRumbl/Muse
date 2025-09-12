from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CompositionBase(BaseModel):
    title: str
    composer_id: UUID


class CompositionCreate(CompositionBase):
    pass


class CompositionUpdate(BaseModel):
    title: str | None = None
    composer_id: UUID | None = None


class Composition(CompositionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
