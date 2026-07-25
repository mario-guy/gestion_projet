"""
Modèle User - Utilisateur (usage personnel, un seul utilisateur).
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(200))
    avatar = Column(String(500))
    timezone = Column(String(50), default="Europe/Paris")
    language = Column(String(10), default="fr")
    theme = Column(String(20), default="light")
    dark_mode = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<User {self.name}>"
