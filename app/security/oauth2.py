from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from app.config.config import setting
from app.db.database import get_db
from app.model import models
from app.model.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE = setting.access_token_expire_minutes


def create_token(payload: dict):
    data_to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    data_to_encode.update({"exp": expire})
    encoded_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


def verify_token(token: str, exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("id")
        if id is None:
            raise exceptions
        token_data = TokenData(id=id)
    except JWTError:
        raise exceptions

    return token_data


def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credential Validation Failed",
                               headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, exceptions=exceptions)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
