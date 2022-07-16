from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..repository import user as userRepository



router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/', response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(database.get_db)):
    return userRepository.create(request, db)

@router.get('/')
def users_list(db: Session = Depends(database.get_db)):
    return userRepository.all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def user(id, db: Session = Depends(database.get_db)):
    return userRepository.show(id, db)