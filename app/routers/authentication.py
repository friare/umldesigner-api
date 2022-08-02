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
@router.post('/register',  status_code=201)
async def create(request: schemas.User, db: Session = Depends(database.get_db)):
    user = authRepository.create(request, db)

    msg = mail.template_new_account.format(request.email, request.email, "https://umldesigner.app/activate-account/"+user.activation_token)

    message = mail.MessageSchema(
        subject="subject",
        recipients=[request.email],
        body=msg,
        subtype="html"
    )

    fm = mail.FastMail(mail.conf)
    await fm.send_message(message)
    return mail.JSONResponse(status_code=200, content={"detail": "Activate your aaccount in your email box."})

@router.post('/token')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return authRepository.login(request, db)

@router.get('/activate/{token}', response_model=schemas.ShowUser)
async def activate(activation_token: str, db: Session = Depends(database.get_db)):
    return authRepository.activate(activation_token, db)

@router.get('/logout')
async def logout(session: Session = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    await session.revoke_session()
    return JSONResponse({})

@router.patch('/reset-password')
def reset(request: schemas.Password, db: Session = Depends(database.get_db), token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return authRepository.reset(request, db, token)

@router.get('/user/me', response_model=schemas.ShowUser, status_code=200)
async def user_me(db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return authRepository.user_me(db, tokendata)