# main.py
from app.config import load_config
from app.logger import logger
from app.models import User, UserResponse
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!"}


@app.get("/db")
def get_db_info():
    logger.info(f"Connecting to database: {config.db.database_url}")
    return {"database_url": config.db.database_url}


config = load_config()

if config.debug:
    app.debug = True
else:
    app.debug = False


@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    return UserResponse(name=user.name, age=user.age, is_adult=user.age >= 18)
