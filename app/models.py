from app.extension import db, LoginManager
from sqlalchemy import Integer, Text, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime
from flask_login import UserMixin

@LoginManager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  firstname: Mapped[str] = mapped_column(String(25), nullable=True)
  lastname: Mapped[str] = mapped_column(String(25), nullable=True)
  avatar: Mapped[str] = mapped_column(String(255), nullable=True, default='avatar.png')
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  games: Mapped[List['Game']] = relationship(back_populates='user', cascade='all, delete-orphan')
  def __repr__(self):
    return f'<User {self.username}>'

class Game(db.Model):
  __tablename__ = 'games'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  platform: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
  genre: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
  status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
  rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
  image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
  note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  user: Mapped['User'] = relationship(back_populates='games')
  def __repr__(self):
    return f'<Game {self.title}>'

