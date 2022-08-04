from fastapi import APIRouter, Depends, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..repository import alert as alertRepo
from ..security import oauth2
from typing import List
from ..repository import mail


router = APIRouter(
    prefix='',
    tags=['Diagram update alert']
)

@router.get('/alert/me', status_code=200, response_model=List[schemas.ShowAlert])
def get_alert(db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return alertRepo.get_alert(db, tokendata)

@router.patch('/alert/read', status_code=200, response_model=schemas.ShowAlert)
def read_alert(request: schemas.Alert, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return alertRepo.read_alert(request, db, tokendata)
