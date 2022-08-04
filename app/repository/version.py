from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta


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
    return version.first()




























def invite(request, project_id, db, tokendata):
    if not re.search(regex, request.collaborator_email):
        raise HTTPException(status_code=400, detail='Incorrect email')

    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True)
    if not project.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    
    author = db.query(models.User).filter(models.User.id == tokendata.id).first()
    user = db.query(models.User).filter(models.User.email == request.collaborator_email).first()
    if not user:
        #create account 
        token = ''
        while True:
            token = ''.join(random.choice(s) for i in range(64))
            d = db.query(models.User).filter(models.User.activation_token  == token).filter(models.User.disabled  == True).first()
            if not d:
                break
        
        #build user
        new_user = models.User(name=request.collaborator_email,  email=request.collaborator_email, password=Hash.bcrypt(token), activation_token=token)
        if not new_user:
            raise HTTPException(status_code=400, detail='Bad Request')
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        #add to project
        token2 = ''
        while True:
            token2 = ''.join(random.choice(s) for i in range(64))
            c = db.query(models.Collaborator).filter(models.Collaborator.validation_token  == 'uvk'+token2).filter(models.Collaborator.is_active  == False).first()
            if not c:
                break

        colab = models.Collaborator(
            role=request.role,
            permission=request.permission,
            project_id=project_id,
            user_id=new_user.id,
            validation_token='uvk'+token2,
            revokation_token='urk'+token2
        )
        db.add(colab)
        db.commit()
        db.refresh(colab)
        return {'data':'new_user_invited', 'activation_token': token, 'collaborator':colab, 'project':project.first(), 'author':author}
    else:
        already_collab = db.query(models.Collaborator).filter(models.Collaborator.user_id == user.id).filter(models.Collaborator.project_id == project_id).first()
        if already_collab:
            raise HTTPException(status_code=201, detail=f"Invitation already sent to this user.")

        if int(user.id) == int(tokendata.id):
            #tu fummes??
            raise HTTPException(status_code=403, detail=f"You'r the owner of this project.")

        token = ''
        while True:
            token = ''.join(random.choice(s) for i in range(64))
            c = db.query(models.Collaborator).filter(models.Collaborator.validation_token  == 'uvk'+token).filter(models.Collaborator.is_active  == False).first()
            if not c:
                break

        colab = models.Collaborator(
            role=request.role,
            permission=request.permission,
            project_id=project_id,
            user_id=user.id,
            validation_token='uvk'+token,
            revokation_token='urk'+token
        )
        db.add(colab)
        db.commit()
        db.refresh(colab)
        return {'data':'old_user_invited', 'collaborator':colab, 'project':project.first(), 'author':author}
