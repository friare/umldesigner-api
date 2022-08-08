from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta
import re 
import random
import string

#global var
s = string.ascii_lowercase
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

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
            user_name=new_user.name,
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
            user_name=user.name,
            validation_token='uvk'+token,
            revokation_token='urk'+token
        )
        db.add(colab)
        db.commit()
        db.refresh(colab)
        return {'data':'old_user_invited', 'collaborator':colab, 'project':project.first(), 'author':author}

def delete(project_id, id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.creator_id == tokendata.id)
    if not project.first():
        raise HTTPException(status_code=403, detail=f"Action not allowed.")

    collaborator = db.query(models.Collaborator).filter(models.Collaborator.project_id == project_id).filter(models.Collaborator.user_id == id)
    if not collaborator.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    
    user = db.query(models.User).filter(models.User.id == collaborator.first().user_id).filter(models.User.disabled == True)

    collaborator.delete(synchronize_session=False)# .update({'is_active': False})
    if user:
        user.delete(synchronize_session=False)

    db.commit()

    return {'detail': 'collaborator successfully deleted.'}
