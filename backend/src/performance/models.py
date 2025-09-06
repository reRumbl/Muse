from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
    

class Performance(Base):
    __tablename__ = 'performance'
    
    composition_id: Mapped[UUID] = mapped_column(ForeignKey('composition.id'))
    ensemble_id: Mapped[UUID] = mapped_column(ForeignKey('ensemble.id'))
