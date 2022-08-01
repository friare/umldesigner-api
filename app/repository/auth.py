from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models, database
from ..schemas import schemas
from ..security import token
from ..security.hashing import Hash
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
import re 

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def create(request: schemas.User ,db: Session):
    if not re.search(regex, request.email):
        raise HTTPException(status_code=400, detail='Incorrect email')
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
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
        data={
            "sub": user.email,
            'id': user.id,
            'disabled': user.disabled,
            'name': user.name
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def reset(request: schemas.Password, db: Session, token_str: str):
    payload = jwt.decode(token_str, token.SECRET_KEY, algorithms=[token.ALGORITHM])
    user = db.query(models.User).filter(models.User.email == payload.get('sub'))

    if not Hash.verify(user.first().password, request.old_password):
        raise HTTPException(status_code=403, detail='Incorrect password')

    # stored_item_data = items[item_id]
    # user_model = models.User(**user.first())
    # update_data = item.dict(exclude_unset=True)
    # updated_item = stored_item_model.copy(update=update_data)
    # items[item_id] = jsonable_encoder(updated_item)
    # return updated_item

    jsonable_encoder(models.User)
    user.update(jsonable_encoder({'password': Hash.bcrypt(request.new_password)}))
    db.commit()
    return user