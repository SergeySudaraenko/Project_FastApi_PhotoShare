from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role
from src.repository.user import ban_user, activate_user
from src.services.auth_service import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/users", tags=["users"])
administrator_access = RoleAccess([Role.admin])


@router.post("/ban/{email}", dependencies=[Depends(administrator_access)])
async def ban_user_route(email: str, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    user = await ban_user(email, db)
    return {"message": f"User {email} has been banned", "user": user}


@router.post("/activate/{email}", dependencies=[Depends(administrator_access)])
async def activate_user_route(email: str, db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    user = await activate_user(email, db)
    return {"message": f"User {email} has been activated", "user": user}
