"""Modèle Meeting - Réunions."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(300))
    is_recurring = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    project = relationship("Project", back_populates="meetings")
