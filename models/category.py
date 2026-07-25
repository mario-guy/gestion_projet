"""Modèle Category - Catégories."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    color = Column(String(7), default="#6366f1")
    created_at = Column(DateTime, server_default=func.now())
