from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from ..repository import blog as blogRepository

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blogRepository.create(request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db: Session = Depends(database.get_db)):
    return blogRepository.delete(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blogRepository.update(id, request, db)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogRepository.get_all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def select(id:int , response: Response, db: Session = Depends(database.get_db)):
    return blogRepository.show(id, db)
    