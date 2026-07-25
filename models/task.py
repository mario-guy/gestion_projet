"""
Modèles Task et SubTask - Tâches et sous-tâches.
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    start_date = Column(Date)
    end_date = Column(Date)
    deadline = Column(Date)
    estimated_duration = Column(Numeric(8, 2), default=0)
    actual_duration = Column(Numeric(8, 2), default=0)
    priority = Column(String(50), default="normal")
    importance = Column(String(50), default="normal")
    urgency = Column(String(50), default="normal")
    difficulty = Column(String(50), default="medium")
    category = Column(String(100))
    responsible = Column(String(200))
    status = Column(String(50), default="backlog")
    labels = Column(String(500))
    progress = Column(Numeric(5, 2), default=0)
    checklist_total = Column(Integer, default=0)
    checklist_done = Column(Integer, default=0)
    position = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    subtasks = relationship("SubTask", back_populates="task", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    time_trackings = relationship("TimeTracking", back_populates="task")

    def __repr__(self):
        return f"<Task {self.title}>"


class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    title = Column(String(300), nullable=False)
    is_done = Column(Boolean, default=False)
    position = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    task = relationship("Task", back_populates="subtasks")

    def __repr__(self):
        return f"<SubTask {self.title}>"
