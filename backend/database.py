# backend/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

# Load DB URLs
POSTGRES_URL = os.getenv("POSTGRES_URL")
SQLITE_URL = os.getenv("SQLITE_URL", "sqlite:///./local.db")

# Determine which DB to use
DB_TYPE = "unknown"

try:
    engine = create_engine(POSTGRES_URL)
    engine.connect()
    DB_TYPE = "postgresql"
    print("✅ Connected to PostgreSQL")
except Exception:
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    DB_TYPE = "sqlite"
    print("⚠️ PostgreSQL not available. Using SQLite.")

# Session and base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Add this function to make get_db work
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
