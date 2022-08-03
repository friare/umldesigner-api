from fastapi import APIRouter, Depends, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..repository import invitation as invitationRepo
from ..security import oauth2
from typing import List
from ..repository import mail


router = APIRouter(
    prefix='',
    tags=['Digram versions']
)

@router.post('/version/fork/{id}', status_code=200, response_model=schemas.ShowResponse)
def accept(id: int, db: Session = Depends(database.get_db)):
    data = invitationRepo.accept(token, db)

@router.post('/version/push/{id}', status_code=200, response_model=schemas.ShowResponse)
def reject_as_user(token: str, db: Session = Depends(database.get_db)):
    data = invitationRepo.reject_as_user(token, db)

@router.get('diagram/version', status_code=200, response_model=schemas.ShowResponse)
def accept(id: int, db: Session = Depends(database.get_db)):
    data = invitationRepo.accept(token, db)

@router.put('/version/update/{id}', status_code=200, response_model=schemas.ShowResponse)
def reject_as_user(token: str, db: Session = Depends(database.get_db)):
    data = invitationRepo.reject_as_user(token, db)
