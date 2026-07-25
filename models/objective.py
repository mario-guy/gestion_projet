"""Modèle Objective - Objectifs."""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

class Objective(Base):
    __tablename__ = "objectives"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    target_date = Column(Date)
    achieved_date = Column(Date)
    progress = Column(Numeric(5, 2), default=0)
    status = Column(String(50), default="todo")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    project = relationship("Project", back_populates="objectives")
