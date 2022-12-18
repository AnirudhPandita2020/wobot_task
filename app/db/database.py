from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import config

setting = config.setting

SQL_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(setting.database_username, setting.database_password,
                                                     setting.database_hostname + ":" + setting.database_port,
                                                     setting.database_name)

engine = create_engine(SQL_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
