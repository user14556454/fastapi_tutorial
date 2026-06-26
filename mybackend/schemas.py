from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(Post):
    pass

class ResponsePost(Post):
    id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: ResponsePost
    votes: int

class User(BaseModel):
    email: EmailStr
    password: str

class CreateUser(User):
    pass

class Validation(BaseModel):
    email: EmailStr
    passwrd: str

class TokenData(BaseModel):
    username: str | None = None

class Vote(BaseModel):
    post_id: int
    vote_dir: Literal[0, 1]