from datetime import date
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
    

class Record(Base):
    __tablename__ = 'record'
    
    title: Mapped[str]
    manufacturer_id: Mapped[UUID] = mapped_column(ForeignKey('company.id'))


class RecordPerformance(Base):
    __tablename__ = 'record_performance'
    
    record_id: Mapped[UUID] = mapped_column(ForeignKey('record.id'))
    performance_id: Mapped[UUID] = mapped_column(ForeignKey('performance.id'))
    

class RecordRelease(Base):
    __tablename__ = 'record_release'
    
    record_id: Mapped[UUID] = mapped_column(ForeignKey('record.id'))
    release_date: Mapped[date]
    wholesale_supplier_id: Mapped[UUID] = mapped_column(ForeignKey('company.id'))
    wholesale_price: Mapped[int]
    retail_price: Mapped[int]
    last_year_sold: Mapped[int]
    this_year_sold: Mapped[int]
    in_stock: Mapped[int]
