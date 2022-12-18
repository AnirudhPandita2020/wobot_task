from fastapi import FastAPI

from app.controller import TodoController, UserController
from app.db.database import engine
from app.model import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="TODO List(Wobot task)",
    description="Task for Python Internship",
    version="1.0.0",
    contact={
        "name": "Anirudh Pandita",
        "url": "https://www.linkedin.com/in/anirudh-pandita-a0b532200/",
        "email": "kppkanu@gmail.com"
    }
)

app.include_router(TodoController.router)
app.include_router(UserController.router)
