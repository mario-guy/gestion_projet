"""Modèle Reminder - Rappels."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from models.base import Base

class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(200), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
