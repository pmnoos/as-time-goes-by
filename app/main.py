from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .database import Base, engine
from . import models
from .routers import router
from .auth.routes import auth_router
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
import os


load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="As Time Goes By")

# Middleware MUST come before everything else
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "changeme"))

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
app.include_router(auth_router)

# Admin auth
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        print(f"[DEBUG] Admin login attempt: username={username}, password={password}")
        print(f"[DEBUG] ENV: ADMIN_USERNAME={os.getenv('ADMIN_USERNAME')}, ADMIN_PASSWORD={os.getenv('ADMIN_PASSWORD')}")
        if username == os.getenv("ADMIN_USERNAME") and \
           password == os.getenv("ADMIN_PASSWORD"):
            request.session["admin"] = True
            print("[DEBUG] Admin login successful!")
            return True
        print("[DEBUG] Admin login failed!")
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

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
        models.Post.author_id,
        models.Post.created_at,
    ]
    column_searchable_list = [models.Post.title, models.Post.slug]
    column_sortable_list = [models.Post.created_at, models.Post.title]
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

# Mount admin AFTER middleware
authentication_backend = AdminAuth(secret_key=os.getenv("SECRET_KEY", "changeme"))
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title="As Time Goes By — Admin",
)

admin.add_view(PostAdmin)
admin.add_view(CommentAdmin)
admin.add_view(UserAdmin)
admin.add_view(TagAdmin)

@app.get("/energy")
def energy(request: Request):
    return templates.TemplateResponse("energy/index.html", {"request": request})