"""Modèle Risk - Risques."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

class Risk(Base):
    __tablename__ = "risks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    probability = Column(Numeric(5, 2), default=0)
    impact = Column(Numeric(5, 2), default=0)
    criticality = Column(Numeric(5, 2), default=0)
    mitigation_plan = Column(Text)
    status = Column(String(50), default="identified")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    project = relationship("Project", back_populates="risks")
