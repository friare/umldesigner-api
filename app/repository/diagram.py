from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta
import random
import string
s = string.ascii_lowercase


def create(request, project_id, type, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.is_active == True).first()
    if project:
        if int(project.creator_id) == int(tokendata.id):
            d = db.query(models.Diagram).filter(models.Diagram.project_id  == project_id).filter(models.Diagram.label  == request.label).first()
            if d:
                raise HTTPException(status_code=400, detail=f"Such diagram already exist. Please change label.")

            token = ''
            while True:
                token = ''.join(random.choice(s) for i in range(32))
                d = db.query(models.Diagram).filter(models.Diagram.public_acces_token  == token).first()
                if not d:
                    break
            new_diagram = models.Diagram(
                type=type, 
                label=request.label,
                plain_text=request.plain_text,
                xml_image="",
                public_acces_token=token,
                date_creation=datetime.now(), 
                author_id=tokendata.id,
                project_id=project_id)
            db.add(new_diagram)
            db.commit()
            db.refresh(new_diagram)
            return new_diagram 
        else:
            print("oo")
            raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")
    else:
        raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")

def get_all(project_id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.is_active == True).first()
    if project:
        if int(project.creator_id) == int(tokendata.id):
            diagrams = db.query(models.Diagram).filter(models.Diagram.project_id  == project_id).all()
            return diagrams 
        else:
            raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")
    else:
        raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")

def get(project_id, id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.is_active == True).first()
    if project:
        if int(project.creator_id) == int(tokendata.id):
            diagrams = db.query(models.Diagram).filter(models.Diagram.project_id  == project_id).filter(models.Diagram.id  == id).first()
            return diagrams 
        else:
            raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")
    else:
        raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")

def delete(project_id, id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.is_active == True).first()
    if project:
        if int(project.creator_id) == int(tokendata.id):
            diagrams = db.query(models.Diagram).filter(models.Diagram.project_id  == project_id).filter(models.Diagram.id  == id).delete(synchronize_session=False)
            db.commit()
            return {'detail': 'Diagram successfully deleted.'}
        else:
            raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")
    else:
        raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")

def update(project_id, id, request, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.is_active == True).first()
    if project:
        if int(project.creator_id) == int(tokendata.id):
            diagram = db.query(models.Diagram).filter(models.Diagram.id == id).filter(models.Diagram.project_id == project_id)
            if not diagram.first():
                raise HTTPException(status_code=404, detail=f"This diagram do not exist.")
            diagram.update({'label': request.label, 'plain_text': request.plain_text, 'xml_image': request.xml_image})
            db.commit()
            return diagram.first()
        else:
            raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")
    else:
        raise HTTPException(status_code=403, detail=f"You're neither author nor collaborator on this project.")

