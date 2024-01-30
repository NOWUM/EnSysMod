from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import User
from ensysmod.schemas import UserCreate
from tests.utils.utils import random_string


def generate_credentials() -> dict[str, str]:
    return {"username": random_string(), "password": random_string()}


def user_create_request(username: str | None = None, password: str | None = None) -> UserCreate:
    if username is not None and password is not None:
        return UserCreate(username=username, password=password)
    return UserCreate(**generate_credentials())


def new_user(db: Session, *, username: str | None = None, password: str | None = None) -> User:
    return crud.user.create(db=db, obj_in=user_create_request(username=username, password=password))
