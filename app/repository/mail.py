from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List
from dotenv import load_dotenv
import os

#load_dotenv('./.env')

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
   #MAIL_USERNAME     = os.getenv("MAIL_USERNAME"),
   MAIL_USERNAME      = "",
   MAIL_PASSWORD      = "",
   MAIL_SERVER        = "",
   MAIL_FROM          = "uda@uda.dev",
   #MAIL_PASSWORD     = os.getenv('MAIL_PASSWORD'),
   #MAIL_FROM         = os.getenv("MAIL_USERNAME"),
   MAIL_PORT         = 587,
   #MAIL_SERVER       = os.getenv('MAIL_SERVER'),
   MAIL_FROM_NAME    = "UMLDesigner",
   MAIL_TLS          = True,
   MAIL_SSL          = False,
   USE_CREDENTIALS   = True,
   VALIDATE_CERTS    = True,
   TEMPLATE_FOLDER   = './app/mail/template'
)


baseURL = "http://localhost:8080"
ACCOUNT_ACTIVATION_LINK             = baseURL+"/activation-de-compte/{}"
INVITATION_ACCEPT_LINK              = baseURL+"/accepter-invitation/{}"
INVITATION_REJECT_LINK              = baseURL+"/rejeter-invitation/{}"
INVITATION_ACCEPT_LINK_AND_REGISTER = baseURL+"/invitation-et-inscription/accepter/{}/{}"
INVITATION_REJECT_LINK_AND_REGISTER = baseURL+"/invitation-et-inscription/rejeter/{}/{}"
PASSWORD_FORGET_LINK                 = baseURL+"/mot-de-passe-oublie/{}"
