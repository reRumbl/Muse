from uuid import UUID
from pydantic import BaseModel, ConfigDict


class RecordBase(BaseModel):
    title: str
    manufacturer_id: UUID
    

class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    title: str | None = None
    manufacturer_id: UUID | None = None


class Record(RecordBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
