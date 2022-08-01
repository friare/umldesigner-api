from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta


def get_all(db, tokendata):
    project = db.query(models.Project).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True).all()
    return project

def create(request, db, tokendata):
    new_project = models.Project(title=request.title, description=request.description, date_creation=datetime.now(), creator_id=tokendata.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project 

def get(id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    return project

def delete(id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True)
    if not project.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    project.update({'is_active': False})
    db.commit()
    return {'detail': 'Project successfully deleted.'}

def update(request, id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True)
    if not project.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    project.update({'title': request.title, 'description': request.description})
    db.commit()
    return project.first()

def invited_project(db, tokendata):
    project = db.query(models.Project).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True).all()
    return project
