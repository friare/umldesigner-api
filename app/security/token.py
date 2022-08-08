from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from ..schemas import schemas
from ..repository import auth


SECRET_KEY = "d5931bf879a3cbacace54c759f28f707bce8384d9231c6e206c2fb7886faded0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        if auth.is_token_blacklisted(token):
            print('---------\n---------\n----------\n----------\n--------')
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: str = payload.get("id")
        name: str = payload.get("name")
        disabled: str = payload.get("disabled")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, disabled=disabled, name=name, email=email)
        return token_data
    except JWTError:
        raise credentials_exception