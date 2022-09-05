from fastapi import APIRouter, Depends, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..core.uml_codex import bundle as guideonCode
from typing import List
from fastapi import status, HTTPException


router = APIRouter(
    prefix='',
    tags=['UML/Code']
)

@router.post('/uml-class/java', status_code=200)
def java(request: schemas.CodeXML):
    result = "guideonCode"
    try:
        result = guideonCode.to_java(request.xml_uml)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f'An error occur. May be you diagram attributes are note typed as expected for java language')
    return result

@router.post('/uml-class/python', status_code=200)
def python(request: schemas.CodeXML):
    result = "guideonCode"
    try:
        result = guideonCode.to_python(request.xml_uml)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f'An error occur')
    return result

@router.post('/uml-class/laravel_migration', status_code=200)
def laravel_migration(request: schemas.CodeXML):
    return "soon"