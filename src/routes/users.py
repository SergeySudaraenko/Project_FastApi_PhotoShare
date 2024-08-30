from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user import ban_user, activate_user, get_user_by_email
from src.database.db import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/ban/{email}")
async def ban_user_route(email: str, db: AsyncSession = Depends(get_db)):
    user = await ban_user(email, db)
    return {"message": f"User {email} has been banned", "user": user}

@router.post("/activate/{email}")
async def activate_user_route(email: str, db: AsyncSession = Depends(get_db)):
    user = await activate_user(email, db)
    return {"message": f"User {email} has been activated", "user": user}
