from typing import Optional

from fastapi import Depends, HTTPException
from libgravatar import Gravatar
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import Role, User
from src.schemas.users import UserSchema, UserUpdateSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    statmnt = select(User).filter_by(email=email)
    user = await db.execute(statmnt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession) -> User:
    # Перевірка кількості користувачів зареєстрованих в БД
    result = await db.execute(select(func.count()).select_from(User))
    total_users_count = result.scalar()
    # Отримання аватара
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(f"Error getting Gravatar image: {err}")
    # Визначення ролі
    role = Role.admin if total_users_count == 0 else Role.user
    # Створення нового користувача
    new_user = User(**body.model_dump(), avatar=avatar, role=role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_name(name: str, db: AsyncSession) -> Optional[User]:
    stmt = select(User).filter_by(username=name)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
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


async def update_user(name: str, body: UserUpdateSchema, db):
    user = await get_user_by_name(name, db)
    if user:
        if body.username:
            user.username = body.username
        if body.email:
            user.email = body.email
        if body.avatar:
            user.avatar = body.avatar
        await db.commit()
        await db.refresh(user)
        return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


async def ban_user(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return user


async def activate_user(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    await db.commit()
    await db.refresh(user)
    return user
