
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DATETIME
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True) 
    password = Column(String)
    activation_token = Column(String, nullable=True)
    password_renewer_token = Column(String, nullable=True)
    disabled = Column(Boolean, default=True)

    projects = relationship('Project', back_populates='creator', cascade="all,delete")
    alerts = relationship('Alert', back_populates='project_owner', cascade="all,delete")

class Project(Base): 
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String) 
    date_creation = Column(DATETIME)
    is_active = Column(Boolean, default=True)
    creator_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates='projects', cascade="all,delete")
    diagrams = relationship('Diagram', back_populates='project', cascade="all,delete")
    collaborators = relationship('Collaborator', back_populates='project', cascade="all,delete")

class Collaborator(Base):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    permission = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    validation_token = Column(String)
    revokation_token = Column(String)
    is_active = Column(Boolean, default=False)

    project = relationship('Project', back_populates='collaborators', cascade="all,delete")

class Diagram(Base):
    __tablename__ = "diagrams"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    label = Column(String)
    plain_text = Column(Text)
    xml_image = Column(Text)
    public_acces_token = Column(String)
    date_creation = Column(DATETIME)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    project = relationship('Project', back_populates='diagrams', cascade="all,delete")
    versions = relationship('Version', back_populates='diagram', cascade="all,delete")


class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    id_colaborator = Column(Integer, ForeignKey('collaborators.id'))
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    label = Column(String)
    date_creation = Column(DATETIME)
    input_text = Column(Text)
    xml_image = Column(Text)
    public_link = Column(Text)

    diagram = relationship('Diagram', back_populates='versions', cascade="all,delete")
    
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, default="Nouvelle version")
    label = Column(String, default="Version1.0")
    id_version = Column(Integer, ForeignKey('versions.id'))
    project_owner_id = Column(Integer, ForeignKey('users.id'))
    id_project = Column(Integer, ForeignKey('projects.id'))
    date_update = Column(DATETIME)
    already_read = Column(Boolean, default=False)

    project_owner = relationship('User', back_populates='alerts', cascade="all,delete")
    

class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String)
    content = Column(String)
    date_creation = Column(DATETIME)
    linked_diagram_id = Column(Integer, ForeignKey('diagrams.id'))

