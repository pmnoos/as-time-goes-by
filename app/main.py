from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .database import Base, engine
from . import models
from .routers import router
from .auth.routes import auth_router
from sqladmin import Admin, BaseView, ModelView, expose
from sqladmin.authentication import AuthenticationBackend
from sqladmin.filters import BooleanFilter, ForeignKeyFilter, OperationColumnFilter, StaticValuesFilter
from starlette.requests import Request
from starlette.responses import RedirectResponse
import os
from pathlib import Path
from .schemas import CATEGORIES
from .templates_config import templates


load_dotenv()

APP_ROOT = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="As Time Goes By")

# Middleware MUST come before everything else
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "changeme"))


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse(APP_ROOT / "static/robots.txt", media_type="text/plain")

@app.get("/googlef4d68b79c1c91576.html", include_in_schema=False)
async def google_verification():
    return FileResponse(
        APP_ROOT / "static/googlef4d68b79c1c91576.html",
        media_type="text/html"
    )
@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse(APP_ROOT / "static/sitemap.xml", media_type="application/xml")
# Mount static for main app and energy_calculator

app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")
app.mount(
    "/energy-static",
    StaticFiles(directory=APP_ROOT / "energy_calculator" / "static"),
    name="energy_static",
)

# Include routers
app.include_router(router)
app.include_router(auth_router)

# Import and include energy_calculator router
from .energy_calculator.router import router as energy_router
app.include_router(energy_router)

# Admin auth
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if username == os.getenv("ADMIN_USERNAME") and \
           password == os.getenv("ADMIN_PASSWORD"):
            request.session["admin"] = True
            print("[DEBUG] Admin login successful!")
            return True
        print("[DEBUG] Admin login failed!")
        return False

    @app.get("/admin/logout")
    async def admin_logout(request: Request):
        request.session.clear()
        return RedirectResponse(url="/", status_code=302)

    async def authenticate(self, request: Request):
        if not request.session.get("admin"):
            return RedirectResponse(url="/admin/login", status_code=302)
        return True

# Admin views
class PostAdmin(ModelView, model=models.Post):
    name = "Post"
    name_plural = "Posts"
    icon = "fa-solid fa-file-alt"
    column_list = [
        models.Post.id,
        models.Post.title,
        models.Post.slug,
        models.Post.category,
        models.Post.author_id,
        models.Post.created_at,
    ]
    column_searchable_list = [models.Post.title, models.Post.slug]
    column_sortable_list = [models.Post.created_at, models.Post.title]
    column_filters = [
        ForeignKeyFilter(models.Post.author_id, models.User.username, models.User),
        StaticValuesFilter(models.Post.category, values=list(CATEGORIES)),
        OperationColumnFilter(models.Post.created_at),
    ]
    can_create = True
    can_edit = True
    can_delete = True


class CommentAdmin(ModelView, model=models.Comment):
    name = "Comment"
    name_plural = "Comments"
    icon = "fa-solid fa-comments"
    column_list = [
        models.Comment.id,
        models.Comment.body,
        models.Comment.author_id,
        models.Comment.post_id,
        models.Comment.created_at,
    ]
    column_sortable_list = [models.Comment.created_at]
    column_filters = [
        ForeignKeyFilter(models.Comment.author_id, models.User.username, models.User),
        ForeignKeyFilter(models.Comment.post_id, models.Post.title, models.Post),
        OperationColumnFilter(models.Comment.created_at),
    ]
    can_create = False
    can_edit = False
    can_delete = True


class UserAdmin(ModelView, model=models.User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"
    column_list = [
        models.User.id,
        models.User.username,
        models.User.email,
        models.User.created_at,
    ]
    column_searchable_list = [models.User.username, models.User.email]
    can_create = False
    can_edit = False
    can_delete = True
    form_excluded_columns = [models.User.password]


class TagAdmin(ModelView, model=models.Tag):
    
    name = "Tag"
    name_plural = "Tags"
    icon = "fa-solid fa-tags"
    column_list = [models.Tag.id, models.Tag.name]
    column_searchable_list = [models.Tag.name]
    can_create = True
    can_edit = True
    can_delete = True

class ContactMessageAdmin(ModelView, model=models.ContactMessage):
    name = "Contact Message"
    name_plural = "Contact Messages"
    icon = "fa-solid fa-envelope"
    column_list = [
        models.ContactMessage.id,
        models.ContactMessage.name,
        models.ContactMessage.email,
        models.ContactMessage.subject,
        models.ContactMessage.created_at,
        models.ContactMessage.is_read,
    ]
    column_searchable_list = [
        models.ContactMessage.name,
        models.ContactMessage.email,
        models.ContactMessage.subject,
    ]
    column_sortable_list = [
        models.ContactMessage.created_at,
        models.ContactMessage.is_read,
    ]
    column_filters = [
        BooleanFilter(models.ContactMessage.is_read),
        OperationColumnFilter(models.ContactMessage.created_at),
    ]
    can_create = False
    can_edit = True
    can_delete = True
# Mount admin AFTER middleware
authentication_backend = AdminAuth(secret_key=os.getenv("SECRET_KEY", "changeme"))
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title="As Time Goes By — Admin",
)

class ViewSiteLink(BaseView):
    name = "View Live Site"
    icon = "fa-solid fa-arrow-up-right-from-square"

    @expose("/view-site", methods=["GET"])
    async def view_site(self, request: Request):
        return RedirectResponse(url="/blog")


admin.add_view(PostAdmin)
admin.add_view(CommentAdmin)
admin.add_view(UserAdmin)
admin.add_view(TagAdmin)
admin.add_view(ContactMessageAdmin)
admin.add_base_view(ViewSiteLink)


