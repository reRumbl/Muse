from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.auth.service import AuthService
from src.auth.schemas import User
from src.auth.models import UserModel, UserRole
from src.auth.utils import decode_access_token
from src.auth.constants import SUB
from src.dependencies import SessionDep
from src.auth.exceptions import UnauthorizedUserException
from src.exceptions import ForbiddenException


def get_auth_service(session: SessionDep):
    return AuthService(session)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep, session: SessionDep) -> User:
    payload = await decode_access_token(session, token)
    user = await session.get(UserModel, payload[SUB])
    if not user:
        raise UnauthorizedUserException()
    
    user_schema = User.model_validate(user)
    return user_schema


CurrentUserDep = Annotated[User, Depends(get_current_user)]  


async def only_admin_user(user: CurrentUserDep) -> User:
    if user.role != UserRole.admin:
        raise ForbiddenException()
    return user


OnlyAdminUserDep = Annotated[User, Depends(only_admin_user)]
