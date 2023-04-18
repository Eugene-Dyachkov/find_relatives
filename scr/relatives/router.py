from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, and_

from uuid import uuid4

from auth.router import get_current_user
from engine import get_async_session
from models import Relatives, Link, User
from .shemas import CreateRelatives

relatives_router = APIRouter(prefix="/relatives", tags=['Relatives'])

@relatives_router.get("/hello")
async def hello():
    return {"Hello": "relatives"}


@relatives_router.post('/create', name='Create relatives')
async def add_user(relatives: CreateRelatives,
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session)
):
    if relatives.death_data is None and relatives.birth_data is None:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="One of the dates must be filled in"
        )

    db_relative = await check_relative(relatives, session)
    print(db_relative)
    if db_relative is None:
        id = uuid4()
        stmt = insert(Relatives).values(id = id, **relatives.dict())
        await session.execute(stmt)
        stmt = insert(Link).values(user_id = user.id, relatives_id= id)
        await session.execute(stmt)
        await session.commit()
        return HTTPException(
            status_code= status.HTTP_200_OK,
            detail="Relative add")

    # return db_relative.fetchone()[0]

async def check_relative(relatives, session):
    try:
        stmt = select(Relatives).where(and_(
            Relatives.last_name == relatives.last_name,
            Relatives.first_name == relatives.first_name,
            Relatives.sity == relatives.sity))
        r = await session.execute(stmt)
        return r.fetchone()[0]
    except:
        return None
