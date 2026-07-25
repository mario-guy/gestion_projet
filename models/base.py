"""
Base de données SQLAlchemy - Configuration et session.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from config import DATABASE_URL, DB_PATH
import os

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Retourne une session DB."""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def init_db():
    """Crée toutes les tables si elles n'existent pas."""
    # Activer les clés étrangères pour SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
