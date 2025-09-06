from uuid import UUID
from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class EnsembleType(Enum):
    orchestra = 'orchestra'
    group = 'group'
    quartet = 'quartet'
    quintet = 'quintet'
    

class Ensemble(Base):
    __tablename__ = 'ensemble'
    
    name: Mapped[str]
    type: Mapped[EnsembleType]


class EnsembleMember(Base):
    __tablename__ = 'ensemble_member'
    
    ensemble_id: Mapped[UUID] = mapped_column(ForeignKey('ensemble.id'), nullable=False)
    musician_id: Mapped[UUID] = mapped_column(ForeignKey('musician.id'), nullable=False)
