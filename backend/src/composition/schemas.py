from uuid import UUID
from pydantic import BaseModel


class CompositionBase(BaseModel):
    name: str
    composer_id: UUID


class CompositionCreate(CompositionBase):
    pass


class CompositionUpdate(BaseModel):
    name: str | None = None
    composer_id: UUID | None = None


class Composition(CompositionBase):
    id: UUID
