"""
Service CRUD générique pour toutes les entités.
"""
from typing import Type, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc


class CRUDService:
    """Service CRUD de base."""

    def __init__(self, model: Type):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[Any]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 1000) -> List[Any]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_all_ordered(self, db: Session, order_by: str = "id", desc_order: bool = False) -> List[Any]:
        col = getattr(self.model, order_by, self.model.id)
        if desc_order:
            return db.query(self.model).order_by(desc(col)).all()
        return db.query(self.model).order_by(asc(col)).all()

    def create(self, db: Session, **kwargs) -> Any:
        obj = self.model(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, id: int, **kwargs) -> Optional[Any]:
        obj = self.get(db, id)
        if not obj:
            return None
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        obj = self.get(db, id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True

    def count(self, db: Session) -> int:
        return db.query(self.model).count()

    def filter_by(self, db: Session, **kwargs) -> List[Any]:
        query = db.query(self.model)
        for key, value in kwargs.items():
            if value is not None and hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()
