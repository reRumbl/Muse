from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

# --- Fixing Pylance issues ---
if TYPE_CHECKING:
    from src.ensemble.models import EnsembleModel
    from src.composition.models import CompositionModel
    from src.record.models import RecordModel


class PerformanceModel(Base):
    __tablename__ = 'performance'
    
    composition_id: Mapped[UUID] = mapped_column(ForeignKey('composition.id'))
    ensemble_id: Mapped[UUID] = mapped_column(ForeignKey('ensemble.id'))
    
    ensemble: Mapped['EnsembleModel'] = relationship(
        'EnsembleModel', 
        back_populates='performances',
        lazy='selectin', 
        passive_deletes=True
    )
    composition: Mapped['CompositionModel'] = relationship(
        'CompositionModel', 
        back_populates='performances',
        lazy='selectin', 
        passive_deletes=True
    )
    records: Mapped[list['RecordModel']] = relationship(
        'RecordModel', 
        secondary='record_performance',
        back_populates='performances',
        lazy='selectin', 
        passive_deletes=True
    )
