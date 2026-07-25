"""Modèle Bookmark - Signets."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from models.base import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    url = Column(String(1000), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
