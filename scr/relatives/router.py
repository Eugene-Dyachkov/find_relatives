from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, and_, or_

from uuid import uuid4

from auth.router import get_current_user
from engine import get_async_session
from models import Relatives, Link, User
from .shemas import CreateRelatives
from tasks.tasks import send_notification


relatives_router = APIRouter(prefix="/relatives", tags=['Relatives'])


@relatives_router.post('/create', name='Create relatives')
async def add_user(relatives: CreateRelatives,
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session)
):
    id = uuid4()
    if relatives.death_data is None and relatives.birth_data is None:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="One of the dates must be filled in"
        )
    db_relative = await check_relative(relatives, session)
    if db_relative is None:
        return await new_relatives(user, session, relatives, id)
    # new_descendant = await add_descendant(user, db_relative.id, session)

    # if new_descendant is None:
    #             raise HTTPException(
    #         status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Internal server error"
    #     )
    descendant = await find_descendant(db_relative.id, session)
    users_emails = []
    for user_email in descendant:
        users_emails.append(user_email.email)
        send_notification.delay(user_email.email, user.email)

    return {"We found possible relatives of yours": users_emails}

async def check_relative(relatives, session):
    try:
        stmt = select(Relatives).where(
            and_(
            Relatives.last_name == relatives.last_name,
            Relatives.first_name == relatives.first_name,
            Relatives.sity == relatives.sity),
            or_(
            Relatives.birth_data == relatives.birth_data,
            Relatives.death_data == relatives.death_data)
        )
        r = await session.execute(stmt)
        return r.fetchone()[0]
    except:
        return None


async def new_relatives(user, session, relatives, id):

    stmt = insert(Relatives).values(id = id, **relatives.dict())
    await session.execute(stmt)
    stmt = insert(Link).values(user_id = user.id, relatives_id= id)
    await session.execute(stmt)
    await session.commit()
    return HTTPException(
        status_code= status.HTTP_200_OK,
        detail="Relative add")

async def find_descendant(relatives_id, session):

    stmt = select(User).join(Link, and_(Link.relatives_id == relatives_id, User.id == Link.user_id))
    r = await session.execute(stmt)
    return r.scalars().all()


async def add_descendant(user, relatives_id,session):
    try:
        stmt = insert(Link).values(user_id = user.id, relatives_id = relatives_id)
        result = await session.execute(stmt)
        await session.commit()
        return HTTPException(
        status_code= status.HTTP_200_OK,
        detail="Descendant add")
    except:
        return None
