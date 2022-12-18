# wobot_task
Todo list api using fastapi framework and PostgreSQL Database.
To run the project, Follow the procedure as shown below:
  1. Git clone the project.
  2. Create an .env file in the main project directory
  3. Add the following content with your local machine credentials
  DATABASE_HOSTNAME=localhost
  DATABASE_PORT=5432
  DATABASE_PASSWORD=<PASSWORD>
  DATABASE_NAME=todo-db
  DATABASE_USERNAME=<USERNAME>
  SECRET_KEY=<SECRET KEY>
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=60
  4. In the terminal write the following command
      uvicorn app.main:app 
  5. head over to http://127.0.0.1:8000/docs for the documentation
