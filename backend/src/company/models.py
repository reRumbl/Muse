from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from src.database import Base

# --- Fixing Pylance issues ---
if TYPE_CHECKING:
    from src.record.models import RecordModel, ReleaseModel


class CompanyModel(Base):
    __tablename__ = 'company'
    
    name: Mapped[str]
    address: Mapped[str]
    
    records: Mapped[list['RecordModel']] = relationship(
        'RecordModel',
        back_populates='manufacturer',
        lazy='selectin', 
        passive_deletes=True
    )
    releases: Mapped[list['ReleaseModel']] = relationship(
        'ReleaseModel',
        back_populates='wholesale_supplier',
        lazy='selectin', 
        passive_deletes=True
    )
