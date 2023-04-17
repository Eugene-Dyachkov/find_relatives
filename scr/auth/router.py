from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, update

from models import User
from engine import get_async_session
from .shemas import IdPassUser, Token, TokenData, UserSchema
from .hasher import veify_password

from datetime import datetime, timedelta
from jose import JWTError, jwt

from config import ACCESS_MIN, ALGORITHM, SECRET


auth_router = APIRouter(prefix="/auth", tags=['Authorization'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    uuid = token_data.id
    user = await get_user_by_jwt(uuid, session)
    if user is None:
        raise credentials_exception
    if user.active is False:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Account not active",
    )
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoed_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoed_jwt


async def get_user_by_jwt(id:str, session):

    query = select(User).where(User.id == id)
    try:
        result = await session.execute(query)
        user = result.fetchone()[0]
        return user
    except:
        return False


async def get_user_by_email(email:str, session):

    query = select(User).where(User.email == email)
    try:
        result = await session.execute(query)
        user = result.fetchone()[0]
        return user
    except:
        return False


async def auth_user(email: str, password: str, session):
    user = await get_user_by_email(email, session)
    if not user:
        return False
    if not veify_password(password, user.hashed_password):
        return False

    return user

@auth_router.post("/token")
async def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user = await auth_user(from_data.username, from_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token_expires = timedelta(minutes=int(ACCESS_MIN))
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta= access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/activate")
async def activate_accoutn(h_password: str, email: str, session: AsyncSession = Depends(get_async_session)):

    active = await activate(h_password, email, session)
    return active


async def activate(h_password, email, session):
    stmt = update(User).where(User.email == email).values(active = True)
    await session.execute(stmt)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Account activated!",
        )
