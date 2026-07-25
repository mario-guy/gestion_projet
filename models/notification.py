"""Modèle Notification - Notifications."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from models.base import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    link = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
