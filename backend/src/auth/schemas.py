from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, SecretStr
from pydantic import field_validator, ValidationInfo
from src.auth.models import UserRole
from src.auth.exceptions import PasswordsDidNotMatchException


class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime


class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema
    
    
class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenRequest(BaseModel):
    token: str


class BlackListToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Same as "orm_mode = True"
    
    id: UUID
    expire: datetime
    created_at: datetime


class UserBase(BaseModel):
    username: str
    

class UserRegister(UserBase):
    password: SecretStr
    confirm_password: SecretStr
    role: UserRole
    
    @field_validator('confirm_password')
    def verify_password_match(cls, v: SecretStr, info: ValidationInfo):
        password: SecretStr = info.data.get('password', '')

        if v.get_secret_value() != password.get_secret_value():
            raise PasswordsDidNotMatchException()

        return v


class UserLogin(UserBase):
    password: SecretStr
    

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)  # Same as "orm_mode = True"
    
    id: UUID
    role: UserRole
