# Script to print all unique category values in the posts table
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Post

def main():
    db: Session = SessionLocal()
    categories = db.query(Post.category).distinct().all()
    print("Unique categories in posts:")
    for (cat,) in categories:
        print(f"- {cat}")
    db.close()

if __name__ == "__main__":
    main()
