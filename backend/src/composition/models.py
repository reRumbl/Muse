from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
    

class Composition(Base):
    __tablename__ = 'composition'
    
    title: str
    composer_id: Mapped[UUID] = mapped_column(ForeignKey('musician.id'))
