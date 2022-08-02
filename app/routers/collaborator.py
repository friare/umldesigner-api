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
    tags=['Collaborator']
)

@router.post('/collaborator/invite/{project_id}', status_code=200, response_model=schemas.ShowComplexColab)
async def invite_on_project(request: schemas.Collaborator, project_id: int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    data = projectRepo.invited_project(request, project_id, db, tokendata)
    if data.data == "old_user_invited":
        print(data)
        # msg = mail.invitation_to_project.format(request.email, request.email, "https://umldesigner.app/activate-account/"+user.activation_token)

        # message = mail.MessageSchema(
        #     subject="subject",
        #     recipients=[request.email],
        #     body=msg,
        #     subtype="html"
        # )

        # fm = mail.FastMail(mail.conf)
        # await fm.send_message(message)
        # return mail.JSONResponse(status_code=200, content={"detail": "Activate your aaccount in your email box."})
    else:
        print(data)
        #send other mail

@router.delete('/collaborator/{project_id}/{id}', status_code=200, response_model=schemas.ShowResponse)
def delete_project(id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return projectRepo.delete(id, db, tokendata)
