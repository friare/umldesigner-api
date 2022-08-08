from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta


def get_all(db, tokendata):
    project = db.query(models.Project).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True).all()
    return project

def get_invite(db, tokendata):
    project = db.query(models.Project).join(models.Project.collaborators).filter(models.Project.creator_id != tokendata.id).filter(models.Collaborator.user_id == tokendata.id).filter(models.Project.is_active == True).filter(models.Collaborator.is_active == True).all()
    return project

def create(request, db, tokendata):
    p = db.query(models.Project).filter(models.Project.title  == request.title).filter(models.Project.creator_id  == tokendata.id).filter(models.Project.is_active == True).first()
    if p:
        raise HTTPException(status_code=400, detail=f"Such project already exist. Please change title.")

    new_project = models.Project(title=request.title, description=request.description, date_creation=datetime.now(), creator_id=tokendata.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    colab = models.Collaborator(
        role="ADMIN",
        permission="ADMIN",
        project_id=new_project.id,
        user_id=tokendata.id,
        user_name=tokendata.name,
        validation_token="",
        revokation_token="",
        is_active = True
    )
    db.add(colab)
    db.commit()
    db.refresh(colab)

    return new_project 

def get(id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    return project

def get_invite_id(id, db, tokendata):
    project = db.query(models.Project).join(models.Project.collaborators).filter(models.Project.id == id).filter(models.Project.creator_id != tokendata.id).filter(models.Collaborator.user_id == tokendata.id).filter(models.Project.is_active == True).filter(models.Collaborator.is_active == True).first()
    if not project:
        raise HTTPException(status_code=403, detail=f"You dont have access to this project.")
    return project

def delete(id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.creator_id == tokendata.id)
    if not project.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    project.delete(synchronize_session=False)# .update({'is_active': False})
    db.commit()
    return {'detail': 'Project successfully deleted.'}

def update(request, id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True)
    if not project.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    project.update({'title': request.title, 'description': request.description})
    db.commit()
    return project.first()