"""
This module sets up the SQLAlchemy database connection and provides a dependency function to get the database session.

The `SQLALCHEMY_DATABASE_URL` constant specifies the SQLite database file to use.

The `engine` object is created using `create_engine()` and configured to use the SQLite database.

The `SessionLocal` object is a sessionmaker that creates database sessions, with autocommit and autoflush disabled.

The `Base` object is a declarative base class that can be used to define SQLAlchemy models.

The `get_db()` function is a dependency that provides a database session to be used in other parts of the application. It creates a new session, yields it, and then closes the session when the function completes.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
