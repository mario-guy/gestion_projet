"""
Modèle Project - Projet.
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, index=True)
    description = Column(Text)
    client = Column(String(200))
    company = Column(String(200))
    team = Column(String(200))
    responsible = Column(String(200))
    department = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    actual_end_date = Column(Date)
    budget = Column(Numeric(12, 2), default=0)
    cost = Column(Numeric(12, 2), default=0)
    status = Column(String(50), default="draft")
    progress = Column(Numeric(5, 2), default=0)
    priority = Column(String(50), default="normal")
    complexity = Column(String(50), default="medium")
    color = Column(String(7), default="#6366f1")
    logo = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    objectives = relationship("Objective", back_populates="project", cascade="all, delete-orphan")
    meetings = relationship("Meeting", back_populates="project", cascade="all, delete-orphan")
    time_trackings = relationship("TimeTracking", back_populates="project")

    def __repr__(self):
        return f"<Project {self.name}>"
