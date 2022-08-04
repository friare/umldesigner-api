from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time, timedelta


#--------------------------------
#--------------------------------

class CollaboratorRole(str, Enum):
    guest      = "INVITE"
    admin      = "ADMIN"

class CollaboratorPermission(str, Enum):
    write      = "LECTURE ET ECRITURE"
    read       = "LECTURE SEULE"
    admin      = "ADMIN"

class Collaborator(BaseModel):
    role: CollaboratorRole
    permission: CollaboratorPermission
    collaborator_email: str

class ShowCollaborator(BaseModel):
    id: int
    role: str
    permission: str
    project_id: int
    user_id: int
    is_active: int

    class Config():
        orm_mode = True

class ShowComplexColab(BaseModel):
    data: str
    validation_token: str
    revokation_token: str
    collaborator: ShowCollaborator
    

class Diagram(BaseModel):
    label: str = "new diagram"
    plain_text: str = ""

class DiagramUpdate(BaseModel):
    label: str = "new diagram"
    plain_text: str = ""
    xml_image: str = "<UMLDiagram></UML>"

class ShowDiagram(BaseModel):
    id: int
    type: str
    label: str
    plain_text: str
    xml_image: str
    public_acces_token: str
    date_creation: datetime
    author_id: int
    project_id: int

    class Config():
        orm_mode = True


class Project(BaseModel):
    title: str = "uml project"
    description: str

class ShowProject(BaseModel):
    id: int
    title: str
    description: str
    date_creation: datetime
    is_active: bool
    creator_id: int
    diagrams: List[ShowDiagram] = []
    collaborators: List[ShowCollaborator] = []

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str = "PlumpSparrow"
    email: str = "example@mail.com"
    password: str

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    projects: List[ShowProject] = []
    # alerts: List[Alert] = []

    class Config():
        orm_mode = True


class Version(BaseModel):
    diagram_id: int = 2547896

class Version2(BaseModel):
    input_text: str
    xml_image: str

class ShowVersion(BaseModel):
    id: int
    id_colaborator: int
    diagram_id: int
    label: str = "version1.0"
    date_creation: datetime
    input_text: str
    xml_image: str
    public_link: str

    class Config():
        orm_mode = True

#---

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

class Email(BaseModel):
    email: str = "example@mail.com"

#---

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


class DiagramType(str, Enum):
    use_case        = "USE_CASE"
    class_diag      = "CLASS"
    sequence_diag   = "SEQUENCE"
    object_diag     = "OBJECT"


class UMLText(BaseModel):
    text: str

class ShowUMLSchema(BaseModel):
    xml: str

    class Config():
        orm_mode = True