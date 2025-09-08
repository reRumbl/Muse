from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from src.database import Base

# --- Fixing Pylance issues ---
if TYPE_CHECKING:
    from src.ensemble.models import EnsembleModel
    from src.composition.models import CompositionModel


class MusicianType(Enum):
    performancer = 'performancer'
    composer = 'composer'
    conductor = 'conductor'
    supervisor = 'supervisor'


class MusicianModel(Base):
    __tablename__ = 'musician'
    
    name: Mapped[str]
    surname: Mapped[str]
    type: Mapped[MusicianType]
    
    ensembles: Mapped[list['EnsembleModel']] = relationship(
        'EnsembleModel', 
        secondary='ensemble_member',
        back_populates='musicians',
        lazy='selectin', 
        passive_deletes=True
    )
    compositions: Mapped[list['CompositionModel']] = relationship(
        'CompositionModel', 
        back_populates='musician',
        lazy='selectin', 
        passive_deletes=True
    )
