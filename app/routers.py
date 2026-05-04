
from fastapi import APIRouter, Depends, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db
from .auth.dependencies import get_current_user, require_user
from .templates_config import templates
from collections import namedtuple
import shutil
import re
from pathlib import Path
from .schemas import CATEGORIES

router = APIRouter()

# Energy Calculator Page
@router.get("/energy-calculator", response_class=HTMLResponse)
def energy_calculator_page(request: Request, current_user=None):
    return templates.TemplateResponse(request, "energy-calculator.html", {"request": request, "current_user": current_user})

# ...existing code...

@router.get("/blog/category/{category}", response_class=HTMLResponse)
def blog_category_page(
    category: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    page: int = 1,
):
    # Validate category
    valid_categories = [c[0] for c in CATEGORIES]
    print(f"[DEBUG] Incoming category: '{category}'")
    print(f"[DEBUG] Valid categories: {valid_categories}")
    if category not in valid_categories:
        print("[DEBUG] Category not found! Returning 404.")
        raise HTTPException(status_code=404, detail="Category not found")
    per_page = 6
    total = db.query(models.Post).filter(models.Post.category == category).count()
    posts = (
        db.query(models.Post)
        .filter(models.Post.category == category)
        .order_by(models.Post.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    total_pages = (total + per_page - 1) // per_page
    return templates.TemplateResponse(request, "home.html", {
        "posts": posts,
        "current_user": current_user,
        "page": page,
        "total_pages": total_pages,
        "category": category,
    })


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return re.sub(r"^-+|-+$", "", text)


def get_or_create_tags(db: Session, tag_names: list[str]) -> list:
    tags = []
    for name in tag_names:
        tag = db.query(models.Tag).filter(models.Tag.name == name).first()
        if not tag:
            tag = models.Tag(name=name)
            db.add(tag)
            db.flush()
        tags.append(tag)
    return tags


# HTML pages
@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(request, "landing.html", {
        "current_user": current_user,
    })


@router.get("/blog", response_class=HTMLResponse)
def home_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    page: int = 1,
):
    per_page = 6
    total = db.query(models.Post).count()
    posts = (
        db.query(models.Post)
        .order_by(models.Post.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    total_pages = (total + per_page - 1) // per_page
    return templates.TemplateResponse(request, "home.html", {
        "posts": posts,
        "current_user": current_user,
        "page": page,
        "total_pages": total_pages,
    })
    per_page = 6
    total = db.query(models.Post).count()
    posts = (
        db.query(models.Post)
        .order_by(models.Post.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    total_pages = (total + per_page - 1) // per_page
    return templates.TemplateResponse(request, "home.html", {
        "request": request,
        "posts": posts,
        "current_user": current_user,
        "page": page,
        "total_pages": total_pages,
    })

@router.get("/posts/new", response_class=HTMLResponse)
def new_post_page(request: Request, current_user=Depends(require_user)):
    return templates.TemplateResponse(request, "create.html", {"request": request, "current_user": current_user})


@router.get("/posts/{slug}", response_class=HTMLResponse)
def post_page(slug: str, request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post.id)
        .order_by(models.Comment.created_at.asc())
        .all()
    )
    return templates.TemplateResponse(request, "post.html", {
        "request": request,
        "post": post,
        "current_user": current_user,
        "comments": comments,
    })

@router.post("/posts/new", response_class=HTMLResponse)
def create_post_page(
    request: Request,
    title: str = Form(...),
    body: str = Form(...),
    category: str = Form(...),
    tags: str = Form(""),
    cover_image: UploadFile = File(None),
    cover_caption: str = Form(default=""),
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    slug = slugify(title)
    existing = db.query(models.Post).filter(models.Post.slug == slug).first()
    if existing:
        return templates.TemplateResponse(request, "create.html", {
            "request": request,
            "current_user": current_user,
            "error": "A post with that title already exists"
        })

    image_path = None
    if cover_image and cover_image.filename:
        upload_dir = Path("app/static/uploads")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / cover_image.filename
        with file_path.open("wb") as f:
            shutil.copyfileobj(cover_image.file, f)
        image_path = f"/static/uploads/{cover_image.filename}"

    tag_names = [t.strip() for t in tags.split(",") if t.strip()]
    post_tags_list = get_or_create_tags(db, tag_names)
    post = models.Post(
        title=title,
        slug=slug,
        body=body,
        category=category,
        cover_image=image_path,
        cover_caption=cover_caption.strip() or None,
        author_id=current_user.id,
        tags=post_tags_list,
    )
    db.add(post)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/search", response_class=HTMLResponse)
def search(
    request: Request,
    q: str = "",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    posts = []
    if q:
        posts = (
            db.query(models.Post)
            .filter(
                models.Post.title.ilike(f"%{q}%") |
                models.Post.body.ilike(f"%{q}%")
            )
            .order_by(models.Post.created_at.desc())
            .all()
        )
    return templates.TemplateResponse(request, "search.html", {
        "posts": posts,
        "current_user": current_user,
        "q": q,
    })

@router.get("/users/{username}", response_class=HTMLResponse)
def author_page(
    username: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    author = db.query(models.User).filter(models.User.username == username).first()
    if not author:
        raise HTTPException(status_code=404, detail="User not found")
    posts = (
        db.query(models.Post)
        .filter(models.Post.author_id == author.id)
        .order_by(models.Post.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(request, "author.html", {
        "author": author,
        "posts": posts,
        "current_user": current_user,
    })


@router.post("/posts/{slug}/comments", response_class=HTMLResponse)
def add_comment(
    slug: str,
    request: Request,
    body: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = models.Comment(
        body=body,
        post_id=post.id,
        author_id=current_user.id,
    )
    db.add(comment)
    db.commit()
    return RedirectResponse(url=f"/posts/{slug}", status_code=303)


@router.post("/posts/{slug}/comments/{comment_id}/delete", response_class=HTMLResponse)
def delete_comment(
    slug: str,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if comment.author_id != current_user.id and (not post or post.author_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not your comment or post")
    db.delete(comment)
    db.commit()
    return RedirectResponse(url=f"/posts/{slug}", status_code=303)

@router.get("/posts/{slug}/edit", response_class=HTMLResponse)
def edit_post_page(slug: str, request: Request, db: Session = Depends(get_db), current_user=Depends(require_user)):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")
    return templates.TemplateResponse(request, "edit.html", {
        "post": post,
        "current_user": current_user,
    })


@router.post("/posts/{slug}/edit", response_class=HTMLResponse)
def edit_post(
    slug: str,
    request: Request,
    title: str = Form(...),
    body: str = Form(...),
    category: str = Form(...),
    tags: str = Form(""),
    cover_image: UploadFile = File(default=None),
    cover_caption: str = Form(default=""),
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")

    post.title = title
    post.slug = slugify(title)
    post.body = body
    post.category = category

    if cover_image and cover_image.filename and cover_image.size > 0:
        upload_dir = Path("app/static/uploads")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / cover_image.filename
        with file_path.open("wb") as f:
            shutil.copyfileobj(cover_image.file, f)
        post.cover_image = f"/static/uploads/{cover_image.filename}"

    tag_names = [t.strip() for t in tags.split(",") if t.strip()]
    post.tags = get_or_create_tags(db, tag_names)
    post.cover_caption = cover_caption.strip() or None
    db.commit()
    return RedirectResponse(url=f"/posts/{post.slug}", status_code=303)

@router.post("/posts/{slug}/delete", response_class=HTMLResponse)
def delete_post_page(
    slug: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")
    db.delete(post)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/mortgage", response_class=HTMLResponse)
def mortgage_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(request, "mortgage.html", {
        "request": request,
        "current_user": current_user,
    })


@router.post("/mortgage", response_class=HTMLResponse)
def mortgage_calculate(
    request: Request,
    current_user=Depends(get_current_user),
    principal: float = Form(...),
    annual_rate: float = Form(...),
    years: int = Form(...),
    check_year: int = Form(...),
    extra_repayment: float = Form(default=0),
    page: int = Form(default=1),
):
    monthly_rate = annual_rate / 100 / 12
    total_payments = years * 12
    check_payment = check_year * 12

    if monthly_rate == 0:
        monthly_payment = principal / total_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / \
                          ((1 + monthly_rate) ** total_payments - 1)

    Row = namedtuple('Row', ['month', 'year', 'interest', 'principal', 'balance', 'extra', 'accelerated'])

    # Standard schedule
    standard_schedule = []
    balance = principal
    total_interest_standard = 0

    for month in range(1, total_payments + 1):
        interest = balance * monthly_rate
        principal_paid = monthly_payment - interest
        balance -= principal_paid
        total_interest_standard += interest
        if balance < 0:
            balance = 0
        standard_schedule.append(Row(
            month=month,
            year=(month - 1) // 12 + 1,
            interest=round(interest, 2),
            principal=round(principal_paid, 2),
            balance=round(balance, 2),
            extra=0,
            accelerated=False,
        ))

    # Accelerated schedule with extra repayments
    accelerated_schedule = []
    balance = principal
    total_interest_accelerated = 0
    actual_months = 0

    for month in range(1, total_payments + 1):
        if balance <= 0:
            break
        interest = balance * monthly_rate
        principal_paid = monthly_payment - interest
        extra = min(extra_repayment, balance - principal_paid)
        extra = max(extra, 0)
        balance -= (principal_paid + extra)
        total_interest_accelerated += interest
        actual_months = month
        if balance < 0:
            balance = 0
        accelerated_schedule.append(Row(
            month=month,
            year=(month - 1) // 12 + 1,
            interest=round(interest, 2),
            principal=round(principal_paid, 2),
            balance=round(balance, 2),
            extra=round(extra, 2),
            accelerated=True,
        ))

    balance_at_check_standard = standard_schedule[check_payment - 1].balance if check_payment <= total_payments else 0
    balance_at_check_accelerated = accelerated_schedule[check_payment - 1].balance if check_payment <= len(accelerated_schedule) else 0

    months_saved = total_payments - actual_months
    years_saved = months_saved // 12
    remaining_months_saved = months_saved % 12
    interest_saved = total_interest_standard - total_interest_accelerated

    # Pagination on accelerated schedule if extra repayments, else standard
    schedule = accelerated_schedule if extra_repayment > 0 else standard_schedule

    per_page = 24
    total_pages = (len(schedule) + per_page - 1) // per_page
    page = max(1, min(page, total_pages))
    paginated = schedule[(page - 1) * per_page: page * per_page]

    return templates.TemplateResponse(request, "mortgage.html", {
        "request": request,
        "current_user": current_user,
        "schedule": paginated,
        "monthly_payment": round(monthly_payment, 2),
        "total_interest_standard": round(total_interest_standard, 2),
        "total_interest_accelerated": round(total_interest_accelerated, 2),
        "total_cost": round(principal + total_interest_standard, 2),
        "total_cost_accelerated": round(principal + total_interest_accelerated, 2),
        "balance_at_check_standard": round(balance_at_check_standard, 2),
        "balance_at_check_accelerated": round(balance_at_check_accelerated, 2),
        "interest_saved": round(interest_saved, 2),
        "months_saved": months_saved,
        "years_saved": years_saved,
        "remaining_months_saved": remaining_months_saved,
        "actual_months": actual_months,
        "principal": principal,
        "annual_rate": annual_rate,
        "years": years,
        "check_year": check_year,
        "extra_repayment": extra_repayment,
        "page": page,
        "total_pages": total_pages,
        "per_page": per_page,
    })
    
@router.get("/about", response_class=HTMLResponse)
def about_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(request, "about.html", {
        "request": request,
        "current_user": current_user,
    })


@router.get("/about-me", response_class=HTMLResponse)
def about_me_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(request, "about_me.html", {
        "current_user": current_user,
    })
    
    