from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta


def accept(token, db):
    collaborator = db.query(models.Collaborator).filter(models.Collaborator.validation_token == token).filter(models.Collaborator.is_active == False)
    if not collaborator.first():
        raise HTTPException(status_code=404, detail='Not Found.')
    collaborator.update({
        'validation_token': '',
        'revokation_token': '',
        'is_active': True,
    })
    db.commit()
    return {'detail': 'You have acces to this project now.'}

def reject_as_user(token, db):
    collaborator = db.query(models.Collaborator).filter(models.Collaborator.revokation_token == token).filter(models.Collaborator.is_active == False)
    if not collaborator.first():
        raise HTTPException(status_code=404, detail='Not Found.')
    collaborator.delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Rejection set with success.'}


def signup_and_accept(request, token1, token2, db):
    collaborator = db.query(models.Collaborator).filter(models.Collaborator.validation_token == token1).filter(models.Collaborator.is_active == False)
    user = db.query(models.User).filter(models.User.activation_token == token2).filter(models.User.disabled == True)
    if (not collaborator.first()) or (not user.first()):
        raise HTTPException(status_code=404, detail='Not Found.')

    user.update({
        'name': request.name,
        'password': Hash.bcrypt(request.password),
        'activation_token': '',
        'disabled': False
    })

    collaborator.update({
        'validation_token': '',
        'revokation_token': '',
        'is_active': True,
    })

    db.commit()

    #collaborator
    colab = models.Collaborator(
        role="INVIITE",
        permission="LECTURE SEULE",
        project_id=1,
        user_id=user.id,
        validation_token="",
        revokation_token="",
        is_active = True
    )
    db.add(colab)
    db.commit()
    db.refresh(colab)

    return {'detail': 'Geat ! Everything okay.'}

def reject_as_guest(token1, token2, db):
    collaborator = db.query(models.Collaborator).filter(models.Collaborator.revokation_token == token1).filter(models.Collaborator.is_active == False)
    user = db.query(models.User).filter(models.User.activation_token == token2).filter(models.User.disabled == True)
    if (not collaborator.first()) or (not user.first()):
        raise HTTPException(status_code=404, detail='Not Found.')
    collaborator.delete(synchronize_session=False)
    db.commit()
    user.delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Rejection set with success.'}































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
