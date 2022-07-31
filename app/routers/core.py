from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..repository import project as projectRepo
from ..security import oauth2

router = APIRouter(
    prefix='',
    tags=['App']
)

@router.get('/projects/me', status_code=200)
def all_project(response: Response, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    return projectRepo.projectList()

@router.get('/project/{id}', status_code=200)
def get_project(id:int, response: Response, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    return projectRepo.projectList()

@router.post('/project', status_code=200)
def create_project(response: Response, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    return projectRepo.projectList()

@router.delete('/project/{id}', status_code=200)
def delete_project(id:int, response: Response, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    return projectRepo.projectList()

@router.patch('/project/{id}', status_code=200)
def update_project(id:int, response: Response, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    return projectRepo.projectList()
