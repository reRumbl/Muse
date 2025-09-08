from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from src.database import Base

# --- Fixing Pylance issues ---
if TYPE_CHECKING:
    from src.record.models import RecordModel, RecordReleaseModel


class CompanyModel(Base):
    __tablename__ = 'company'
    
    name: Mapped[str]
    address: Mapped[str]
    
    records: Mapped[list['RecordModel']] = relationship(
        'RecordModel',
        back_populates='company',
        lazy='selectin', 
        passive_deletes=True
    )
    releases: Mapped[list['RecordReleaseModel']] = relationship(
        'RecordReleaseModel',
        back_populates='company',
        lazy='selectin', 
        passive_deletes=True
    )
