
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DATETIME
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String) 
    password = Column(String)
    disabled = Column(Boolean, default=True)

    projects = relationship('Project', back_populates='creator')

class Project(Base): 
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String) 
    date_creation = Column(DATETIME)
    creator_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates='projects')

class Diagram(Base):
    __tablename__ = "diagrams"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    label = Column(String)
    input_text = Column(Text)
    xml_image = Column(Text)
    public_link = Column(Text)
    date_creation = Column(DATETIME)
    author_user_id = Column(Integer, ForeignKey('users.id'))

class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String)
    content = Column(String)
    date_creation = Column(DATETIME)
    linked_diagram_id = Column(Integer, ForeignKey('diagrams.id'))

class Collaborator(Base):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    permission = Column(String)

class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    id_colaborator = Column(Integer, ForeignKey('collaborators.id'))
    id_diagram = Column(Integer, ForeignKey('diagrams.id'))
    label = Column(String)
    date_creation = Column(DATETIME)
    input_text = Column(Text)
    xml_image = Column(Text)
    public_link = Column(Text)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    id_version = Column(Integer, ForeignKey('versions.id'))
    id_utilisateur = Column(Integer, ForeignKey('users.id'))
    id_project = Column(Integer, ForeignKey('projects.id'))
    already_read = Column(Boolean, default=True)