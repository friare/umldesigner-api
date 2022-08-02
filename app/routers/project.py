from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..repository import project as projectRepo
from ..security import oauth2
from typing import List
from ..repository import mail


router = APIRouter(
    prefix='',
    tags=['Project']
)

@router.post('/project', status_code=201, response_model=schemas.ShowProject)
def create_project(request: schemas.Project, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return projectRepo.create(request, db, tokendata)

@router.get('/projects/me', status_code=200, response_model=List[schemas.ShowProject])
def all_project(db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return projectRepo.get_all(db, tokendata)

@router.get('/project/me/{id}', status_code=200, response_model=schemas.ShowProject)
def get_project(id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return projectRepo.get(id, db, tokendata)

@router.delete('/project/{id}', status_code=200, response_model=schemas.ShowResponse)
def delete_project(id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return projectRepo.delete(id, db, tokendata)

@router.patch('/project/{id}', status_code=200, response_model=schemas.ShowProject)
def update_project(request: schemas.Project, id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return projectRepo.update(request, id, db, tokendata)
