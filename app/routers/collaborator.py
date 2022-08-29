from fastapi import APIRouter, Depends, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from ..datastruct import models, database
from ..schemas import schemas
from ..repository import collaborator as collaboratorRepo
from ..security import oauth2
from typing import List
from ..repository import mail


router = APIRouter(
    prefix='',
    tags=['Collaborator']
)

@router.post('/collaborator/invite/{project_id}', status_code=200, response_model=schemas.ShowResponse)
async def invite_collaborator(background_tasks: BackgroundTasks, request: schemas.Collaborator, project_id: int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    data = collaboratorRepo.invite(request, project_id, db, tokendata)
    if data['data'] == "old_user_invited":
        body = {
            'author': data['author'].name,
            'project': data['project'].title,
            'access': data['collaborator'].permission,
            'accept_token': mail.INVITATION_ACCEPT_LINK.format(data['collaborator'].validation_token),
            'revoke_token': mail.INVITATION_REJECT_LINK.format(data['collaborator'].revokation_token)
        }

        message = mail.MessageSchema(
            subject="Invitation to work on uml project !",
            recipients=[request.collaborator_email],
            template_body=body,
            subtype="html"
        )

        fm = mail.FastMail(mail.conf)
        background_tasks.add_task(fm.send_message, message, template_name="invite_collaborator.html")
        return mail.JSONResponse(status_code=201, content={"detail": "Invitation sent."})
    else:
        body = {
            'author': data['author'].name,
            'project': data['project'].title,
            'access': data['collaborator'].permission,
            'accept_token': mail.INVITATION_ACCEPT_LINK_AND_REGISTER.format(data['collaborator'].validation_token, data['activation_token'], data['receiver_mail']),
            'revoke_token': mail.INVITATION_REJECT_LINK_AND_REGISTER.format(data['collaborator'].revokation_token, data['activation_token'])
        }

        message = mail.MessageSchema(
            subject="Invitation to work on uml project !",
            recipients=[request.collaborator_email],
            template_body=body,
            subtype="html"
        )

        fm = mail.FastMail(mail.conf)
        background_tasks.add_task(fm.send_message, message, template_name="invite_collaborator.html")
        return mail.JSONResponse(status_code=201, content={"detail": "Invitation sent."})


@router.delete('/collaborator/{project_id}/{id}', status_code=200, response_model=schemas.ShowResponse)
def remove_collaborator(project_id: int, id:int, db: Session = Depends(database.get_db), tokendata = Depends(oauth2.get_current_user)):
    return collaboratorRepo.delete(project_id, id, db, tokendata)
