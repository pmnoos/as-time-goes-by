# Script to update all posts in the database to use valid category values from CATEGORIES
# Usage: uvicorn app.scripts.fix_categories:main --reload

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Post
from app.schemas import CATEGORIES

# Map old/invalid category names to valid ones if needed
CATEGORY_MAP = {
    # Example: 'Finance': 'finance-super',
    # Add more mappings if you have legacy values
}

VALID_CATEGORIES = set(c[0] for c in CATEGORIES)

def main():
    db: Session = SessionLocal()
    posts = db.query(Post).all()
    updated = 0
    for post in posts:
        original = post.category
        # Map or fix category
        new_category = CATEGORY_MAP.get(post.category, post.category)
        if new_category not in VALID_CATEGORIES:
            new_category = 'community-life'  # fallback
        if post.category != new_category:
            post.category = new_category
            updated += 1
    db.commit()
    print(f"Updated {updated} posts with valid categories.")
    db.close()

if __name__ == "__main__":
    main()
