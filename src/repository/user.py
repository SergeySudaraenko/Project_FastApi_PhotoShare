from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas.user import UserDbModel


async def get_user_by_name(name: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(username=name)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def update_user(username, body: UserDbModel, db: AsyncSession):
    user = await get_user_by_name(username, db)

    user.email = body.email
    user.username = body.username

    await db.commit()
    await db.refresh(user)
    return user
