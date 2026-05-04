from app.database import SessionLocal
from app.models import User
from app.auth.utils import hash_password

def reset_password(username, new_password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"User '{username}' not found.")
        return
    user.password = hash_password(new_password)
    db.commit()
    print(f"Password for '{username}' has been reset.")
    db.close()

if __name__ == "__main__":
    reset_password("peter284", "@Bay55watch")
