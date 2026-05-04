from fastapi import APIRouter, Depends, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .utils import hash_password, verify_password, create_access_token
from ..templates_config import templates

auth_router = APIRouter()


@auth_router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})


@auth_router.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = db.query(models.User).filter(
        (models.User.username == username) | (models.User.email == email)
    ).first()
    if existing:
        return templates.TemplateResponse(request, "register.html", {
            "request": request,
            "error": "Username or email already taken"
        })
    user = models.User(
        username=username,
        email=email,
        password=hash_password(password),
    )
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)


@auth_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})


@auth_router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(request, "login.html", {
            "request": request,
            "error": "Invalid username or password"
        })
    token = create_access_token({"sub": str(user.id), "username": user.username})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("access_token", token, httponly=True, max_age=60*60*24)
    return response


@auth_router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

@auth_router.get("/admin-login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {
        "request": request,
        "admin": True,
    })