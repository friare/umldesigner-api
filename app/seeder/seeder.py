from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status, Depends, APIRouter
from ..datastruct import models, database
from ..schemas import schemas
from ..security import token
from ..security.hashing import Hash
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random
import string
import re 
import os


router = APIRouter(
    prefix='',
    tags=['Migration']
)

@router.get('/init', status_code=200)
async def init_db(db: Session = Depends(database.get_db)):
    #variables
    s = string.ascii_lowercase
    load_dotenv('.env')
    ADMIN_NAME                          = os.getenv('ADMIN_NAME')
    ADMIN_EMAIL                         = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD                      = os.getenv('ADMIN_PASSWORD')
    ADMIN_DEFAULT_PROJECT_NAME          = os.getenv('ADMIN_DEFAULT_PROJECT_NAME')
    ADMIN_DEFAULT_PROJECT_DESCRIPTION   = os.getenv('ADMIN_DEFAULT_PROJECT_DESCRIPTION')
    ADMIN_DEFAULT_DIAGRAM_LABEL         = os.getenv('ADMIN_DEFAULT_DIAGRAM_LABEL')
    ADMIN_DEFAULT_DIAGRAM_TEXT          = os.getenv('ADMIN_DEFAULT_DIAGRAM_TEXT')
    ADMIN_DEFAULT_DIAGRAM_XML           = os.getenv('ADMIN_DEFAULT_DIAGRAM_XML')
    ADMIN_DEFAULT_DIAGRAM_TYPE          = os.getenv('ADMIN_DEFAULT_DIAGRAM_TYPE')

    #pipline   
    user = db.query(models.User).filter(models.User.email == ADMIN_EMAIL).first()
    if not user:
        #user
        new_user = models.User(
            name=ADMIN_NAME,  
            email=ADMIN_EMAIL, 
            password=Hash.bcrypt(ADMIN_PASSWORD), 
            activation_token="",
            disabled=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        #project
        new_project = models.Project(
            title=ADMIN_DEFAULT_PROJECT_NAME, 
            description=ADMIN_DEFAULT_PROJECT_DESCRIPTION, 
            date_creation=datetime.now(), 
            creator_id=new_user.id
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        #collaborator
        colab = models.Collaborator(
            role="ADMIN",
            permission="ADMIN",
            project_id=new_project.id,
            user_id=new_user.id,
            validation_token="",
            revokation_token="",
            is_active = True
        )
        db.add(colab)
        db.commit()
        db.refresh(colab)

        #diagram
        token = ''.join(random.choice(s) for i in range(32))
        new_diagram = models.Diagram(
            type=ADMIN_DEFAULT_DIAGRAM_TYPE, 
            label=ADMIN_DEFAULT_DIAGRAM_LABEL,
            plain_text=ADMIN_DEFAULT_DIAGRAM_TEXT,
            xml_image=ADMIN_DEFAULT_DIAGRAM_XML,
            public_acces_token=token,
            date_creation=datetime.now(), 
            author_id=new_user.id,
            project_id=new_project.id)
        db.add(new_diagram)
        db.commit()
        db.refresh(new_diagram)
        return {'detail': 'Pipline: init cobra db  - DONE'}
    else:
        return {'detail': 'This is not Admin device. Report sent to Admin.'}
