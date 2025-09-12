from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.musician.models import MusicianType


class MusicianBase(BaseModel):
    name: str
    surname: str
    type: MusicianType
    

class MusicianCreate(MusicianBase):
    pass


class MusicianUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    type: MusicianType | None = None


class Musician(MusicianBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
