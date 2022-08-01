from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time, timedelta


#--------------------------------
#--------------------------------

class Project(BaseModel):
    title: str
    description: str

class ShowProject(BaseModel):
    title: str
    description: str
    date_creation: datetime
    is_active: bool
    creator_id: int
    # diagrams: List[Diagram] = []

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    projects: List[Project] = []
    # alerts: List[Alert] = []

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str
    disabled: str
    name: str
    email: Optional[str] = None

class ShowResponse(BaseModel):
    detail: str

#--------------------------------
#--------------------------------


class BlogBase(BaseModel):
    title: str
    body: str


class Password(BaseModel):
    old_password: str
    new_password: str


class Blog(BlogBase):
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