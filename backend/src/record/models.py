from datetime import date
from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

# --- Fixing Pylance issues ---
if TYPE_CHECKING:
    from src.performance.models import PerformanceModel
    from src.company.models import CompanyModel
  

class RecordModel(Base):
    __tablename__ = 'record'
    
    title: Mapped[str]
    manufacturer_id: Mapped[UUID] = mapped_column(ForeignKey('company.id'))
    
    releases: Mapped[list['RecordReleaseModel']] = relationship(
        'RecordReleaseModel', 
        back_populates='record',
        lazy='selectin', 
        passive_deletes=True
    )
    performances: Mapped[list['PerformanceModel']] = relationship(
        'PerformanceModel', 
        secondary='record_performance',
        back_populates='records',
        lazy='selectin', 
        passive_deletes=True
    )
    manufacturer: Mapped['CompanyModel'] = relationship(
        'CompanyModel', 
        back_populates='records',
        lazy='selectin', 
        passive_deletes=True
    )


class RecordPerformanceModel(Base):
    __tablename__ = 'record_performance'
    
    record_id: Mapped[UUID] = mapped_column(ForeignKey('record.id'))
    performance_id: Mapped[UUID] = mapped_column(ForeignKey('performance.id'))
    

class RecordReleaseModel(Base):
    __tablename__ = 'record_release'
    
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
        back_populates='records',
        lazy='selectin', 
        passive_deletes=True
    )
    wholesale_supplier: Mapped['CompanyModel'] = relationship(
        'CompanyModel', 
        back_populates='releases',
        lazy='selectin', 
        passive_deletes=True
    )
