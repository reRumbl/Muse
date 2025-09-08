from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

# --- Fixing Pylance issues ---
if TYPE_CHECKING:
    from src.musician.models import MusicianModel
    from src.performance.models import PerformanceModel


class CompositionModel(Base):
    __tablename__ = 'composition'
    
    title: Mapped[str]
    composer_id: Mapped[UUID] = mapped_column(ForeignKey('musician.id'))
    
    composer: Mapped['MusicianModel'] = relationship(
        'MusicianModel', 
        back_populates='compositions',
        lazy='selectin', 
        passive_deletes=True
    )
    performances: Mapped[list['PerformanceModel']] = relationship(
        'PerformanceModel', 
        back_populates='composition',
        lazy='selectin', 
        passive_deletes=True
    )
