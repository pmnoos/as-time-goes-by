"""
Manual migration script to add 'category' column to posts table.
Run this ONCE with: uv run python alembic_add_category.py
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE posts ADD COLUMN category VARCHAR(50) DEFAULT 'community-life'"))
    print("Added 'category' column to posts table.")
