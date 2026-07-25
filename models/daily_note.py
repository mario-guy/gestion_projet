"""Modèle DailyNote - Notes quotidiennes."""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.sql import func
from models.base import Base

class DailyNote(Base):
    __tablename__ = "daily_notes"
    id = Column(Integer, primary_key=True, index=True)
    note_date = Column(Date, nullable=False)
    content = Column(Text)
    mood = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
