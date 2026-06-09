"""
Database initialization and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

# Database path
DB_PATH = os.path.join(os.path.expanduser('~'), '.pixel_edition', 'pixel_edition.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Create engine
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
Session = sessionmaker(bind=engine)


def init_db():
    """
    Initialize database tables
    """
    from core.models import (
        PerformanceProfile,
        GameLibraryEntry,
        CoreConfiguration,
        TensorDeviceInfo,
        DownloadedCore
    )
    
    Base.metadata.create_all(engine)
    print(f"Database initialized at {DB_PATH}")


def get_db_session():
    """
    Get a new database session
    """
    return Session()
