from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta
from . import alert


def all_version(id, db,tokendata):
    version = db.query(models.Version).join(models.Version.diagram).join(models.Diagram.project).join(models.Project.collaborators).filter(models.Diagram.id == id).filter(models.Collaborator.user_id == tokendata.id).filter(models.Collaborator.is_active == True).all()
    return version

def fork(request, db, tokendata):
    diagram = db.query(models.Diagram).join(models.Diagram.project).join(models.Project.collaborators).filter(models.Diagram.id == request.diagram_id).filter(models.Collaborator.user_id == tokendata.id).filter(models.Collaborator.is_active == True).all()
    if len(diagram) <= 0:
        raise HTTPException(status_code=403, detail='Not allowed.')
    old_version = db.query(models.Version).filter(models.Version.diagram_id == request.diagram_id).all()
    main_diagram = db.query(models.Diagram).filter(models.Diagram.id == request.diagram_id).first()
    if not main_diagram:
        raise HTTPException(status_code=404, detail='Not Found.')
    version = models.Version(
        id_colaborator=tokendata.id,
        diagram_id=request.diagram_id,
        label="version-"+str(len(old_version)+1),
        date_creation=datetime.now(),
        input_text=main_diagram.plain_text,
        xml_image=main_diagram.xml_image,
        public_link=main_diagram.public_acces_token+"-version-"+str(len(old_version)+1),
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    alert.new_alert(version, diagram, main_diagram, db, tokendata)
    return version 

def push(id, db, tokendata):
    #for only admin
    version = db.query(models.Version).filter(models.Version.id == id)
    if not version.first():
        raise HTTPException(status_code=403, detail='Not allowed.')

    diagram = db.query(models.Diagram).join(models.Diagram.project).join(models.Project.collaborators).filter(models.Diagram.id == version.first().diagram_id).filter(models.Collaborator.user_id == tokendata.id).filter(models.Project.creator_id == tokendata.id).filter(models.Collaborator.is_active == True).all()
    if len(diagram) <= 0:
        raise HTTPException(status_code=403, detail='Not allowed.')
    
    diagram = db.query(models.Diagram).filter(models.Diagram.id == version.first().diagram_id)
    diagram.update({
        'plain_text': version.first().input_text,
        'xml_image': version.first().xml_image
    })
    db.commit()
    return diagram.first()

def edit_version(request, id, db, tokendata):
    version = db.query(models.Version).filter(models.Version.id == id)
    if not version.first():
        raise HTTPException(status_code=403, detail='Not allowed.')

    diagram = db.query(models.Diagram).join(models.Diagram.project).join(models.Project.collaborators).filter(models.Diagram.id == version.first().diagram_id).filter(models.Collaborator.user_id == tokendata.id).filter(models.Collaborator.is_active == True).all()
    print(len(diagram))
    print(diagram)
    if len(diagram) <= 0:
        raise HTTPException(status_code=403, detail='Not allowed.')

    version.update({
        'input_text': request.input_text,
        'xml_image': request.xml_image
    })
    db.commit()
    alert.update_alert(version, db)
    return version.first()