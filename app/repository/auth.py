from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from .. import models, schemas, database, token
from ..hashing import Hash
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm


def create(request: schemas.User ,db: Session):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if (not user) or (not Hash.verify(user.password, request.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')

    # generate jwt acces token
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def reset(request: schemas.Password ,db: Session, token_str: str):
    payload = jwt.decode(token_str, token.SECRET_KEY, algorithms=[token.ALGORITHM], verify_signature=False)
    user = db.query(models.User).filter(models.User.email == payload.get('email')).first()
    
    if not Hash.verify(user.password, request.old_password):
        raise HTTPException(status_code=status.HTTP_403_FOR_BIDDEN, detail='Incorrect password')

    user.update({'password':Hash.bcrypt(request.new_password)})
    db.commit()
    return user