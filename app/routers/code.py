from fastapi import APIRouter, Depends, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..core.uml_codex import bundle as guideonCode
from typing import List


router = APIRouter(
    prefix='',
    tags=['UML/Code']
)

@router.post('/uml-class/java', status_code=200)
def java(request: str = "<UMLClassDiagram name='umldesigner.app'></UMLClassDiagram>"):
    try:
        return guideonCode.to_java(request)
    except Exception as e:
        return 'An error occur. May be you diagram attributes are note typed as expected for java language'

@router.post('/uml-class/python', status_code=200)
def python(request: str = "<UMLClassDiagram name='umldesigner.app'></UMLClassDiagram>"):
    try:
        return guideonCode.to_python(request)
    except Exception as e:
        return 'An error occur.'

@router.post('/uml-class/laravel_migration', status_code=200)
def laravel_migration(request: str = "<UMLClassDiagram name='umldesigner.app'></UMLClassDiagram>"):
    return "soon"