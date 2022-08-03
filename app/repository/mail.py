from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List
from dotenv import load_dotenv
import os

load_dotenv('.env')

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
   MAIL_USERNAME     = os.getenv('MAIL_USERNAME'),
   MAIL_PASSWORD     = os.getenv('MAIL_PASSWORD'),
   MAIL_FROM         = os.getenv('MAIL_FROM'),
   MAIL_PORT         = int(os.getenv('MAIL_PORT')),
   MAIL_SERVER       = os.getenv('MAIL_SERVER'),
   MAIL_FROM_NAME    = os.getenv('MAIL_FROM_NAME'),
   MAIL_TLS          = os.getenv('MAIL_TLS'),
   MAIL_SSL          = os.getenv('MAIL_SSL'),
   USE_CREDENTIALS   = os.getenv('USE_CREDENTIALS'),
   VALIDATE_CERTS    = os.getenv('VALIDATE_CERTS'),
   TEMPLATE_FOLDER   = os.getenv('MAIL_TEMPLATE_FOLDER')
)

baseURL = os.getenv('FRONT_BASE_URL')
ACCOUNT_ACTIVATION_LINK             = baseURL+os.getenv('ACTIVATE_ACCOUNT')
INVITATION_ACCEPT_LINK              = baseURL+os.getenv('INVITATION_ACCEPT')
INVITATION_REJECT_LINK              = baseURL+os.getenv('INVITATION_REJECT')
INVITATION_ACCEPT_LINK_AND_REGISTER = baseURL+os.getenv('INVITATION_SIGNUP_ACCEPT')
INVITATION_REJECT_LINK_AND_REGISTER = baseURL+os.getenv('INVITATION_SIGNUP_REJECT')