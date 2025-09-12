from datetime import date
from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if TYPE_CHECKING:
    from src.record.models import RecordModel
    from src.company.models import CompanyModel


class ReleaseModel(Base):
    __tablename__ = 'release'
    
    record_id: Mapped[UUID] = mapped_column(ForeignKey('record.id'))
    release_date: Mapped[date]
    wholesale_supplier_id: Mapped[UUID] = mapped_column(ForeignKey('company.id'))
    wholesale_price: Mapped[int]
    retail_price: Mapped[int]
    last_year_sold: Mapped[int]
    this_year_sold: Mapped[int]
    in_stock: Mapped[int]
    
    record: Mapped['RecordModel'] = relationship(
        'RecordModel', 
        back_populates='releases',
        lazy='selectin', 
        passive_deletes=True
    )
    wholesale_supplier: Mapped['CompanyModel'] = relationship(
        'CompanyModel', 
        back_populates='releases',
        lazy='selectin', 
        passive_deletes=True
    )
