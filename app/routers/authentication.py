from fastapi import APIRouter, Depends, status, HTTPException
from ..datastruct import models, database
from ..schemas import schemas
from ..security import token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..repository import auth as authRepository
from fastapi.responses import JSONResponse
from ..security import oauth2
from ..repository import mail

router = APIRouter(
    tags=['Auth'],
    prefix='/auth' 
)

@router.post('/register',  status_code=201, response_model=schemas.ShowResponse)
async def create(request: schemas.User, db: Session = Depends(database.get_db)):
    user = authRepository.create(request, db)

    body = {
        'email': request.email,
        'link': mail.ACCOUNT_ACTIVATION_LINK.format(user.activation_token)
    }

    message = mail.MessageSchema(
        subject="Welcome to UMLDesigner !",
        recipients=[request.email],
        template_body=body,
        subtype="html"
    )

    fm = mail.FastMail(mail.conf)
    await fm.send_message(message, template_name="new_account.html")
    return mail.JSONResponse(status_code=201, content={"detail": "Activate your account in your email box."})

@router.post('/token')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return authRepository.login(request, db)

@router.get('/activate/{token}', response_model=schemas.ShowUser)
async def activate(activation_token: str, db: Session = Depends(database.get_db)):
    return authRepository.activate(activation_token, db)

@router.get('/logout', status_code=200, response_model=schemas.ShowResponse)
async def logout(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    authRepository.add_token_blacklisted(token)
    return {'detail': 'Access Token destroyed. Session closed.'}
    

@router.patch('/reset-password')
def reset(request: schemas.Password, db: Session = Depends(database.get_db), token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return authRepository.reset(request, db, token)

@router.post('/forget-password', response_model=schemas.ShowResponse)
async def reset(request: schemas.Email, db: Session = Depends(database.get_db)):
    token = authRepository.send_reset_password_mail(request, db)
    
    body = {
        'email': request.email,
        'token': mail.PASSWORD_FORGET_LINK.format(token)
    }

    message = mail.MessageSchema(
        subject="Change password request ! ",
        recipients=[request.email],
        template_body=body,
        subtype="html"
    )

    fm = mail.FastMail(mail.conf)
    await fm.send_message(message, template_name="change_password.html")
    return mail.JSONResponse(status_code=200, content={"detail": "Email sent to your mail box."})

@router.get('/user/me', response_model=schemas.ShowUser, status_code=200)
async def user_me(db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return authRepository.user_me(db, tokendata)