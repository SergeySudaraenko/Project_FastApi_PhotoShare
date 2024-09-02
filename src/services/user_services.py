from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository.user import get_user_by_email
from src.database.models import User

async def deactivate_user(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if user:
        user.is_active = False
        await db.commit()
        await db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

async def activate_user(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if user:
        user.is_active = True
        await db.commit()
        await db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
