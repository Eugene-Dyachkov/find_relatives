from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert
from sqlalchemy.exc import IntegrityError

from models import User
from engine import get_async_session
from .shemas import UserSchema

from auth.hasher import veify_password, get_password_hash
from auth.router import get_current_user
from tasks.register_active.tasks import send_email_register
user_router = APIRouter(prefix="/user", tags=['User'])



# registration
@user_router.post('/user/registration', name='Registration', response_model=UserSchema)
async def add_user(user: UserSchema, session: AsyncSession = Depends(get_async_session)):
    u = User()
    user.hashed_password = get_password_hash(user.hashed_password)
    d = user.dict()
    for k in d:
        setattr(u, k, d[k])
    session.add(u)
    await session.commit()
    print(user.email)
    send_email_register.delay(user.hashed_password, user.email, user.username)
    await session.refresh(u)
    return UserSchema.from_orm(u)



@user_router.delete("/user/delete", name='Delete user')
async def delete_user(
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(User).where(User.id == user.id)
    result = await session.execute(stmt)
    return {"status": 200}

@user_router.get('/user/me')
async def jwt_user(user: Annotated[User, Depends(get_current_user)]):
    return user
