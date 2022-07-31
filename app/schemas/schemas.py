from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str


class Password(BaseModel):
    old_password: str
    new_password: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class DiagramType( str, Enum ):
    use_case = "use_case"
    class_diag = "class"
    sequence_diag = "sequence"
    object_diag = "object"


class UMLText(BaseModel):
    text: str

class ShowUMLSchema(BaseModel):
    xml: str

    class Config():
        orm_mode = True

