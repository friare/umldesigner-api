from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List
from dotenv import load_dotenv
import os

load_dotenv('./.env')

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
   MAIL_USERNAME     = os.getenv("MAIL_USERNAME"),
   MAIL_PASSWORD     = os.getenv('MAIL_PASSWORD'),
   MAIL_FROM         = os.getenv('MAIL_FROM'),
   MAIL_PORT         = os.getenv('MAIL_PORT'),
   MAIL_SERVER       = os.getenv('MAIL_SERVER'),
   MAIL_FROM_NAME    = "UMLDesigner",
   MAIL_TLS          = False,
   MAIL_SSL          = True,
   USE_CREDENTIALS   = True,
   VALIDATE_CERTS    = True,
   TEMPLATE_FOLDER   = './app/mail/template'
)

baseURL = "https://umldesigner.app"
ACCOUNT_ACTIVATION_LINK             = baseURL+"/activate-account/{}"
INVITATION_ACCEPT_LINK              = baseURL+"/invitation-accept/{}"
INVITATION_REJECT_LINK              = baseURL+"/invitation-reject/{}"
INVITATION_ACCEPT_LINK_AND_REGISTER = baseURL+"/invitation-and-registration/accept/{}/{}"
INVITATION_REJECT_LINK_AND_REGISTER = baseURL+"/invitation-and-registration/accept/{}/{}"
PASSWORD_FORGET_LINK                 = baseURL+"/password-forget/{}"
