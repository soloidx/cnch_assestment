from contextlib import contextmanager
from typing import Generator
from project.models.database import SessionLocal


# this is for FastAPI
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# this works as a context especially for scripts
@contextmanager
def get_db_context()->Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
