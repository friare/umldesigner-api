from fastapi import APIRouter, Depends, status, HTTPException
from ..datastruct import models, database
from ..schemas import schemas
from ..security import token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..repository import auth as authRepository
from fastapi.responses import JSONResponse


router = APIRouter(
    tags=['Auth'],
    prefix='/auth' 
)
@router.post('/register', response_model=schemas.ShowUser, status_code=201)
def create(request: schemas.User, db: Session = Depends(database.get_db)):
    return authRepository.create(request, db)

@router.post('/token')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return authRepository.login(request, db)

@router.get('/logout')
async def logout(session: Session = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    await session.revoke_session()
    return JSONResponse({})

@router.post('/reset-password')
def reset(request: schemas.Password, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")), session: Session = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return authRepository.reset(request, db, token)
