from uuid import UUID
from pydantic import BaseModel


class RecordBase(BaseModel):
    title: str
    manufacturer_id: UUID
    

class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    title: str | None = None
    manufacturer_id: UUID | None = None


class Record(RecordBase):
    id: UUID
