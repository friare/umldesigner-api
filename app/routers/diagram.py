from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..repository import diagram as diagramRepo
from ..security import oauth2
from typing import List




router = APIRouter(
    prefix='',
    tags=['Diagram']
)

@router.post('/diagram/{project_id}/{type}', status_code=201, response_model=schemas.ShowDiagram)
def create_diagram(request: schemas.Diagram, project_id: int, type: schemas.DiagramType, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return diagramRepo.create(request, project_id, type, db, tokendata)

# @router.post('/diagram/clone/{id}', status_code=200, response_model=List[schemas.ShowProject])
# def create_diagram_version(db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
#     return diagramRepo.get_all(db, tokendata)

@router.get('/diagram/all/{project_id}', status_code=200, response_model=List[schemas.ShowDiagram])
def get_all(project_id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return diagramRepo.get_all(project_id, db, tokendata)

@router.get('/diagram/{project_id}/{id}', status_code=200, response_model=schemas.ShowDiagram)
def get(project_id:int, id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return diagramRepo.get(project_id, id, db, tokendata)

@router.get('/diagram/{token}', status_code=200, response_model=schemas.ShowDiagram)
def get(token: str, db: Session = Depends(database.get_db)):
    return diagramRepo.publicGet(token, db)

@router.delete('/diagram/{project_id}/{id}', status_code=200, response_model=schemas.ShowResponse)
def delete_diagram(project_id: int, id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return diagramRepo.delete(project_id, id, db, tokendata)

@router.put('/diagram/{project_id}/{id}', status_code=200, response_model=schemas.ShowDiagram)
def update_diagram(project_id: int, id:int, request: schemas.DiagramUpdate, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return diagramRepo.update(project_id, id, request, db, tokendata)