"""
Manual migration script to add 'cover_caption' column to posts table.
Run this ONCE with: uv run python alembic_add_cover_caption.py
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Adjust this if your DB URL is different
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE posts ADD COLUMN cover_caption VARCHAR(300)"))
    print("Added 'cover_caption' column to posts table.")
