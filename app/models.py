from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

post_tags = Table(
    "post_tags", Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id",  ForeignKey("tags.id"),  primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String(50), unique=True, nullable=False)
    email      = Column(String(100), unique=True, nullable=False)
    password   = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posts    = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    slug        = Column(String(220), unique=True, nullable=False)
    body        = Column(Text, nullable=False)
    cover_image = Column(String(300), nullable=True)
    cover_caption = Column(String(300), nullable=True)
    category    = Column(String(50), nullable=False, default="community-life")
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())
    author_id   = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    tags   = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")

class Tag(Base):
    __tablename__ = "tags"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    
class Comment(Base):
    __tablename__ = "comments"

    id         = Column(Integer, primary_key=True, index=True)
    body       = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    post_id    = Column(Integer, ForeignKey("posts.id"))
    author_id  = Column(Integer, ForeignKey("users.id"))

    post   = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")    