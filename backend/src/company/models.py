from sqlalchemy.orm import Mapped
from src.database import Base
    

class Company(Base):
    __tablename__ = 'company'
    
    name: Mapped[str]
    address: Mapped[str]
