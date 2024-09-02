from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from src.database.db import get_db
from src.repository import user as repository_users
from src.config.config import settings
from sqlalchemy import select
from src.database.models import User, BlacklistedToken
import logging



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.SECRET_KEY_JWT
    ALGORITHM = settings.ALGORITHM


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def create_access_token(
            self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def create_refresh_token(
            self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        
    async def blacklist_token(self, token: str, expires_at: datetime, db: AsyncSession):
        blacklisted_token = BlacklistedToken(token=token, expires_at=expires_at)
        db.add(blacklisted_token)
        await db.commit()

    async def is_token_blacklisted(self, token: str, db: AsyncSession):
        stmt = select(BlacklistedToken).filter_by(token=token)
        result = await db.execute(stmt)
        blacklisted_token = result.scalar_one_or_none()

        if blacklisted_token and blacklisted_token.expires_at > datetime.utcnow():
            return True
        return False

    async def get_current_user(
            self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Декодируем JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    logging.error("Email not found in JWT payload")
                    raise credentials_exception
            else:
                logging.error("Invalid token scope")
                raise credentials_exception
        except JWTError as e:
            logging.error(f"JWT decoding error: {str(e)}")
            raise credentials_exception


        if await self.is_token_blacklisted(token, db):
            logging.error(f"Token is blacklisted: {token}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token was cancelled",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            logging.error(f"User not found with email: {email}")
            raise credentials_exception

        return user

    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )

    async def is_admin(self, current_user: User = Depends(get_current_user)):
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")


auth_service = Auth()