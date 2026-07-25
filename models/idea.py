"""Modèle Idea - Idées."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from models.base import Base

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    status = Column(String(50), default="backlog")
    priority = Column(String(50), default="normal")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
