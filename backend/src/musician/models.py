from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class MusicianType(Enum):
    performancer = 'performancer'
    composer = 'composer'
    conductor = 'conductor'
    supervisor = 'supervisor'


class Musician(Base):
    name: Mapped[str]
    surname: Mapped[str]
    type: Mapped[MusicianType]
