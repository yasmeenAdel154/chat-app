from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")  # "postgresql://chatuser:strongpassword@localhost:5432/chatdb"

print("DB URL:", DB_URL)

# Use SQLAlchemy sync engine for simplicity
engine = create_engine(DB_URL, pool_pre_ping=True, future=True)

# Session factory (not async)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

Base = declarative_base()


# Dependency for FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
