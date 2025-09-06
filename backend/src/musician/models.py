from enum import Enum
from sqlalchemy.orm import Mapped
from src.database import Base


class MusicianType(Enum):
    performancer = 'performancer'
    composer = 'composer'
    conductor = 'conductor'
    supervisor = 'supervisor'


class Musician(Base):
    __tablename__ = 'musician'
    
    name: Mapped[str]
    surname: Mapped[str]
    type: Mapped[MusicianType]
