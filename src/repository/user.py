from uuid import uuid4

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.db import get_db
from src.database.models import User
from src.schemas.users import UserSchema



async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    statmnt = select(User).filter_by(email=email)
    user = await db.execute(statmnt)
    user = user.scalar_one_or_none()
    return user



async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db. refresh(new_user)
    return new_user

async def get_user_by_name(name: str, db: AsyncSession = Depends(get_db)):
    statmnt = select(User).filter_by(username=name)
    user = await db.execute(statmnt)
    user = user.scalar_one_or_none()
    return user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()



async def confirmed_email(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()



async def update_avatar(email, url: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(email: str, body: UserSchema, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(email, db)
    if user:
        if body.username:
            user.username = body.username
        if body.email:
            user.email = body.email
        if body.password:
            user.password = body.password
        await db.commit()
        await db.refresh(user)
        return user