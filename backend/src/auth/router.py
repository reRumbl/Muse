from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from src.schemas import SuccessResponse
from src.auth.schemas import User, UserRegister, UserLogin, TokenPairResponse, TokenRequest
from src.auth.dependencies import AuthServiceDep

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=User)
async def register(data: UserRegister, auth_service: AuthServiceDep):
    user = await auth_service.register(data) 
    return user


@router.post('/login', response_model=TokenPairResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    auth_service: AuthServiceDep
):
    user_login_data = UserLogin(username=form_data.username, password=SecretStr(form_data.password))
    tokens = await auth_service.login(user_login_data)
    return tokens


@router.post('/logout', response_model=SuccessResponse)
async def logout(data: TokenRequest, auth_service: AuthServiceDep):
    await auth_service.logout(data.token)
    return SuccessResponse(message='Succesfully logout')


@router.get('/users/{user_id}', response_model=User)
async def get_user(user_id: UUID, auth_service: AuthServiceDep):
    user = await auth_service.get(user_id) 
    return user


@router.post('/refresh', response_model=TokenPairResponse)
async def refresh(data: TokenRequest, auth_service: AuthServiceDep):
    tokens = await auth_service.refresh(data.token)
    return tokens
