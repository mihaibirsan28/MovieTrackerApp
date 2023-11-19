from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enums import LinkType

from database.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(256))
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_confirmed = Column(Boolean)

    wishlist = relationship("Wishlist", back_populates="user")
    library = relationship("Library", back_populates="user")
    links = relationship("Link", back_populates="user")


class Wishlist(Base):
    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    imdb_movie_id = Column(String(50), nullable=False)

    user = relationship("User", back_populates="wishlist")


class Library(Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    imdb_movie_id = Column(String(50), nullable=False)

    user = relationship("User", back_populates="library")


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    link_token = Column(String(50), nullable=False)
    link_type = Column(String(50), nullable=False)
    expiry_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="links")