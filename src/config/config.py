import enum
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, func, Enum, ForeignKey, Integer, Boolean, Table, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

class Role(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Role] = mapped_column("role", Enum(Role), default=Role.user, nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

class Photo(Base):
    __tablename__ = 'photos'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    description: Mapped[str] = mapped_column(String(255), index=True)
    created_at: Mapped[datetime] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", backref="photos", lazy="joined")
    photo_tags: Mapped[List["Tag"]] = relationship("Tag", secondary="photo_tag", back_populates="photos")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="photo")

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(50), unique=True)
    photos: Mapped[List["Photo"]] = relationship("Photo", secondary="photo_tag", back_populates="photo_tags")

photo_tag = Table('photo_tag', Base.metadata, Column('photo_id', Integer, ForeignKey('photos.id')),
                  Column('tag_id', Integer, ForeignKey('tags.id')))

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="comments", lazy="joined")
    photo_id: Mapped[int] = mapped_column(Integer, ForeignKey("photos.id"), nullable=False)
    photo: Mapped["Photo"] = relationship("Photo", back_populates="comments")