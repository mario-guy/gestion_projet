"""Modèle TimeTracking - Suivi du temps."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

class TimeTracking(Base):
    __tablename__ = "time_tracking"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer, default=0)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    project = relationship("Project", back_populates="time_trackings")
    task = relationship("Task", back_populates="time_trackings")
