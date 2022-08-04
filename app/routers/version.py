from fastapi import APIRouter, Depends, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..repository import version as versionRepo
from ..security import oauth2
from typing import List
from ..repository import mail


router = APIRouter(
    prefix='',
    tags=['Diagram versions']
)

@router.post('/version/fork', status_code=200, response_model=schemas.ShowVersion)
def clone_diagram(request: schemas.Version, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return versionRepo.fork(request, db, tokendata)

@router.post('/version/push/{id}', status_code=200, response_model=schemas.ShowDiagram)
def push_diagram(id, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return versionRepo.push(id, db, tokendata)

@router.get('/diagram/{id}/version/', status_code=200, response_model=List[schemas.ShowVersion])
def pull_diagram(id: int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return versionRepo.all_version(id, db, tokendata)

@router.put('/version/update/{id}', status_code=200, response_model=schemas.ShowVersion)
def edit_version(request: schemas.Version2, id: str, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return versionRepo.edit_version(request, id, db, tokendata)
