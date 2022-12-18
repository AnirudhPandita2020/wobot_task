from typing import List

from fastapi import Depends, HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.model import models
from app.model.schemas import TodoCreate, TodoListResponse, User
from app.security.oauth2 import get_user

router = InferringRouter(tags=["Todo Controller"])


@cbv(router)
class TodoController(object):
    user: User = Depends(get_user)
    db: Session = Depends(get_db)

    @router.get(path="/todo/fetch", response_model=List[TodoListResponse])
    async def fetch_todo(self):
        return self.db.query(models.TodoList).filter(models.TodoList.userid == self.user.id).all()

    @router.post(path="/todo/add")
    async def add_todo(self, new_task: TodoCreate):
        new_task = models.TodoList(**new_task.dict())
        new_task.userid = self.user.id
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    @router.put(path="/todo/modify")
    async def update_todo(self, taskId: int, task: TodoCreate):
        task_to_update = self.db.query(models.TodoList).filter(models.TodoList.id == taskId)
        if not task_to_update.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exists")
        tas = task_to_update.first()

        if tas.userid != self.user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")

        task_to_update.update(task.dict(), synchronize_session=False)
        self.db.commit()

        return task_to_update.first()

    @router.delete(path="/todo/delete/{taskId}")
    async def delete_todo(self, taskId: int):
        task = self.db.query(models.TodoList).filter(models.TodoList.id == taskId)

        if task.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does not Exists")

        if task.first().userid != self.user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")

        task.delete(synchronize_session=False)
        self.db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
