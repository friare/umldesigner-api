from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta
import random
import string
s = string.ascii_lowercase

def invited_project(request, project_id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == project_id).filter(models.Project.creator_id == tokendata.id).filter(models.Project.is_active == True)
    if not project.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    author = db.quary(models.User).filter(models.User.id == tokendata.id).fist()
    user = db.quary(models.User).filter(models.User.email == request.email).fist()
    if not user:
        #create account 
        token = ''
        while True:
            token = ''.join(random.choice(s) for i in range(64))
            d = db.query(models.User).filter(models.User.activation_token  == token).filter(models.User.disabled  == True).first()
            if not d:
                break
        
        #build user
        new_user = models.User(name=request.email,  email=request.email, password=Hash.bcrypt(token), activation_token=token)
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
            project_id=request.project_id,
            user_id=request.user_id,
            validation_token='uvk'+token,
            revokation_token='urk'+token
        )
        db.add(colab)
        db.commit()
        db.refresh(colab)
        return {'data':'new_user_invited', 'activation_token': token, 'validation_token':validation_token, 'revokation_token':revokation_token, 'collaborator':colab, 'project':project, 'author':author}
    else:
        token = ''
        while True:
            token = ''.join(random.choice(s) for i in range(64))
            c = db.query(models.Collaborator).filter(models.Collaborator.validation_token  == 'uvk'+token).filter(models.Collaborator.is_active  == False).first()
            if not c:
                break

        colab = models.Collaborator(
            role=request.role,
            permission=request.permission,
            project_id=request.project_id,
            user_id=request.user_id,
            validation_token='uvk'+token,
            revokation_token='urk'+token
        )
        db.add(colab)
        db.commit()
        db.refresh(colab)
        return {'data':'old_user_invited', 'validation_token':validation_token, 'revokation_token':revokation_token, 'collaborator':colab, 'project':project, 'author':author}

def delete(id, db, tokendata):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.creator_id == tokendata.id)
    if not project.first():
        raise HTTPException(status_code=404, detail=f"This project do not exist.")
    project.delete(synchronize_session=False)# .update({'is_active': False})
    db.commit()
    return {'detail': 'Project successfully deleted.'}
