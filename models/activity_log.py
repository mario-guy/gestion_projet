"""Modèle ActivityLog - Journal d'activités."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from models.base import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer)
    details = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
