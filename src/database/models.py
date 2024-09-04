import enum
import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy import Column, Float, String, DateTime, func, Enum, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates


class Base(DeclarativeBase):
    pass


# Перерахування ролей
class Role(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


# Модель для користувачів
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user, nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# Модель для фото
class Photo(Base):
    __tablename__ = "photos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", backref="photos")
    photo_tags: Mapped[List["Tag"]] = relationship("Tag", secondary="photo_tag", back_populates="photos")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="photo")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="photo")
    average_rating: Mapped[float] = mapped_column(Float, default=0.0)


# Модель для тегів
class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    photos: Mapped[List["Photo"]] = relationship("Photo", secondary="photo_tag", back_populates="photo_tags")


# Таблиця для зв'язку фото і тегів
photo_tag = Table("photo_tag", Base.metadata, Column("photo_id", Integer, ForeignKey("photos.id")),
                  Column("tag_id", Integer, ForeignKey("tags.id")))


# Модель коментів
class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="comments")
    photo_id: Mapped[int] = mapped_column(Integer, ForeignKey("photos.id"), nullable=False)
    photo: Mapped["Photo"] = relationship("Photo", back_populates="comments")


# Модель для рейтингів
class Rating(Base):
    __tablename__ = "ratings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_id: Mapped[int] = mapped_column(Integer, ForeignKey("photos.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    photo: Mapped["Photo"] = relationship("Photo", back_populates="ratings")
    user: Mapped["User"] = relationship("User")

    @validates('score')
    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise ValueError('Score must be greater or equal 1 and less than 5.')
        return value


# Модель для чорного списку токенів
class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'
    token = Column(String, primary_key=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
