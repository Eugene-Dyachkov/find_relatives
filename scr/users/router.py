from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert
from sqlalchemy.exc import IntegrityError

from models import User, Relatives, Link
from engine import get_async_session
from .shemas import UserSchema, RegisterUser

from auth.hasher import veify_password, get_password_hash
from auth.router import get_current_user
from tasks.register_active.tasks import send_email_register


user_router = APIRouter(prefix="/user", tags=['User'])


# registration
@user_router.post('/user/registration', name='Registration')
async def registration(user: RegisterUser, session: AsyncSession = Depends(get_async_session)):
    user.password = get_password_hash(user.password)
    stmt = insert(User).values(
        username = user.username,
        email = user.email,
        hashed_password = user.password)
    await session.execute(stmt)
    await session.commit()
    send_email_register.delay(user.password, user.email, user.username)
    return HTTPException(
        status_code= status.HTTP_201_CREATED,
        detail="The account is registered, to activate it, follow the instructions that came to the email.")


@user_router.delete("/user/delete", name='Delete user')
async def delete_user(
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(User).where(User.id == user.id)
    result = await session.execute(stmt)
    return HTTPException(
        status_code= status.HTTP_200_OK,
        detail="Account has been deleted")

@user_router.get('/user/me')
async def jwt_user(user: Annotated[User, Depends(get_current_user)]):
    return user
