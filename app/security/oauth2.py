from fastapi import Depends,HTTPException, status
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/swagger/token")

async def get_current_user(token_data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return token.verify_token(token_data, credentials_exception)
