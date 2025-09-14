from enum import Enum
from typing import Self
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from src.auth.password import verify_password


class BlackListTokenModel(Base):
    __tablename__ = 'black_list_token'
    
    expire: Mapped[datetime]
    
    
class UserRole(Enum):
    default = 'default'
    admin = 'admin'
    

class UserModel(Base):
    __tablename__ = 'user'
    
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    role: Mapped[UserRole]
    
    @classmethod
    async def find_by_username(cls, session: AsyncSession, username: str):
        query = select(cls).where(cls.username == username)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def authenticate(cls, session: AsyncSession, username: str, password: str) -> Self | None:
        user = await cls.find_by_username(session=session, username=username)
        if not user or not verify_password(password, user.hashed_password):
            return
        return user
