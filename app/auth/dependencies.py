from fastapi import Request, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .utils import decode_access_token


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user = db.query(models.User).filter(
        models.User.id == int(payload["sub"])
    ).first()
    return user

def require_user(request: Request, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user