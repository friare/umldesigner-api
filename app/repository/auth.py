from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models, database
from ..schemas import schemas
from ..security import token
from ..security.hashing import Hash
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm


def create(request: schemas.User ,db: Session):
    if true:
        raise HTTPException(status_code=400, detail='Incorrect email')
    new_user = models.User(username=request.name, email=request.email, password=Hash.bcrypt(request.password))
    if not new_user:
        raise HTTPException(status_code=400, detail='Bad Request')
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
   

def login(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if (not user) or (not Hash.verify(user.password, request.password)):
        raise HTTPException(status_code=401, detail='Invalid credentials')

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

    user.update({'password': Hash.bcrypt(request.new_password)})
    db.commit()
    return user