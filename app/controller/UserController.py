from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from app.db.database import get_db
from app.model import models
from app.model.schemas import *
from app.security import oauth2
from app.utils import utils

router = InferringRouter(tags=["User Controller"])


@cbv(router)
class UserController(object):
    db: Session = Depends(get_db)

    @router.post(path="/user/create", response_model=User)
    async def create_user(self, user: UserCreate):
        exists_user = self.db.query(models.User).filter(models.User.email == user.email).first()

        if exists_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        user.password = utils.hashing(user.password)
        new_user = models.User(**user.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    @router.post(path="/user/login")
    async def login_user(self, user_cred: OAuth2PasswordRequestForm = Depends()):
        user = self.db.query(models.User).filter(models.User.email == user_cred.username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Creds")

        if not utils.verify(user_cred.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Creds")

        access_token = oauth2.create_token(payload={"id": user.id})

        return {"access_token": access_token, "token_type": "bearer"}
