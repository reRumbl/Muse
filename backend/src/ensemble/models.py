from uuid import UUID
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

# --- Fixing Pylance issues ---
if TYPE_CHECKING:
    from src.musician.models import MusicianModel
    from src.performance.models import PerformanceModel


class EnsembleType(Enum):
    orchestra = 'orchestra'
    group = 'group'
    quartet = 'quartet'
    quintet = 'quintet'
    

class EnsembleModel(Base):
    __tablename__ = 'ensemble'
    
    name: Mapped[str]
    type: Mapped[EnsembleType]
    
    musicians: Mapped[list['MusicianModel']] = relationship(
        'MusicianModel', 
        secondary='ensemble_member',
        back_populates='ensembles',
        lazy='selectin', 
        passive_deletes=True
    )
    performances: Mapped[list['PerformanceModel']] = relationship(
        'PerformanceModel', 
        back_populates='ensemble',
        lazy='selectin', 
        passive_deletes=True
    )


class EnsembleMemberModel(Base):
    __tablename__ = 'ensemble_member'
    
    ensemble_id: Mapped[UUID] = mapped_column(ForeignKey('ensemble.id'), nullable=False)
    musician_id: Mapped[UUID] = mapped_column(ForeignKey('musician.id'), nullable=False)
