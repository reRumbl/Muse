from datetime import date
from uuid import UUID
from pydantic import BaseModel


class ReleaseBase(BaseModel):
    record_id: UUID
    release_date: date
    wholesale_supplier_id: UUID
    wholesale_price: int
    retail_price: int
    last_year_sold: int
    this_year_sold: int
    in_stock: int
    

class ReleaseCreate(ReleaseBase):
    pass


class ReleaseUpdate(BaseModel):
    record_id: UUID | None = None
    release_date: date | None = None
    wholesale_supplier_id: UUID | None = None
    wholesale_price: int | None = None
    retail_price: int | None = None
    last_year_sold: int | None = None
    this_year_sold: int | None = None
    in_stock: int | None = None


class Release(ReleaseBase):
    id: UUID
