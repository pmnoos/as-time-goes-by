from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    body: str
    cover_image: Optional[str] = None

class PostCreate(PostBase):
    tags: Optional[List[str]] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = []

class PostResponse(PostBase):
    id: int
    slug: str
    created_at: datetime
    tags: List[Tag] = []
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class CommentCreate(BaseModel):
    body: str

class CommentResponse(BaseModel):
    id: int
    body: str
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True        
        
CATEGORIES = [
    ("finance-super", "💰 Finance & Super"),
    ("health-wellbeing", "🏥 Health & Wellbeing"),
    ("housing", "🏠 Housing"),
    ("legal-estate", "⚖️ Legal & Estate"),
    ("technology", "📱 Technology"),
    ("community-life", "🤝 Community & Life"),
]

class PostBase(BaseModel):
    title: str
    body: str
    category: str = "community-life"
    cover_image: Optional[str] = None

class PostCreate(PostBase):
    tags: Optional[List[str]] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    category: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = []

class PostResponse(PostBase):
    id: int
    slug: str
    created_at: datetime
    tags: List[Tag] = []
    class Config:
        from_attributes = True        