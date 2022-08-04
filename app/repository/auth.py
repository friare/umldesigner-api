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
import random
import string

#global var
s = string.ascii_lowercase
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def create(request: schemas.User ,db: Session):
    try:
        #email check
        if not re.search(regex, request.email):
            raise HTTPException(status_code=400, detail='Incorrect email')

        #activation token
        token = ''
        while True:
            token = ''.join(random.choice(s) for i in range(64))
            d = db.query(models.User).filter(models.User.activation_token  == token).filter(models.User.disabled  == True).first()
            if not d:
                break
        
        #build user
        new_user = models.User(name=request.name,  email=request.email, password=Hash.bcrypt(request.password), activation_token=token)
        if not new_user:
            raise HTTPException(status_code=400, detail='Bad Request')
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        #return user
        return new_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='Bad Request. Email already taken.')
   
def login(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if user.disabled:
        raise HTTPException(status_code=401, detail='Account disabled. Please activate it in your mail address.')
 
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

def activate(activation_token, db):
    user = u = db.query(models.User).filter(models.User.activation_token == activation_token).filter(models.User.disabled == True)
    if not user.first():
        raise HTTPException(status_code=404, detail=f"This resource no longer exist.")
    user.update({'activation_token':'', 'disabled':False})
    db.commit()
    return u.first()

def reset(request: schemas.Password, db: Session, token_str: str):
    payload = jwt.decode(token_str, token.SECRET_KEY, algorithms=[token.ALGORITHM])
    user = db.query(models.User).filter(models.User.email == payload.get('sub')).filter(models.User.disabled == False)

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

def user_me(db, tokendata):
    user = db.query(models.User).filter(models.User.email == tokendata.email).filter(models.User.disabled == False).first()
    if not user:
        raise HTTPException(status_code=404, detail='Not found')
    return user

def send_reset_password_mail(request, db):
    user = db.query(models.User).filter(models.User.email == request.email)
    if not user.first():
        raise HTTPException(status_code=404, detail='Not found')
    token = ''
    while True:
        token = ''.join(random.choice(s) for i in range(64))
        d = db.query(models.User).filter(models.User.password_renewer_token  == token).filter(models.User.disabled  == True).first()
        if not d:
            break
    user.update({
        'disabled': True,
        'password_renewer_token': token
    })
    db.commit()
    return token

def add_token_blacklisted(token: str) -> bool:
    with open('./app/security/blacklist.ako', 'a') as file:
        file.write(f'{token};')
    return True

def is_token_clacklisted(token: str) -> bool:
    with open('./app/security/blacklist.ako') as file:
        content = file.read()
        array = content[:-1].split(';')
        if token in array:
            return True
    return False