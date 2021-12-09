import random
import string
from typing import Dict, List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import User
from ensysmod.schemas import UserCreate, UserUpdate


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_float_numbers(size: int = 10) -> List[float]:
    return [random.uniform(0, 1) for _ in range(size)]


def user_authentication_headers(
        *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    data = {"username": username, "password": password}

    r = client.post("/auth/login", data=data, headers={"content-type": "application/x-www-form-urlencoded"})
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_username(
        *, client: TestClient, username: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given username.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_username(db, username=username)
    if not user:
        user_in_create = UserCreate(username=username, password=password)
        crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, username=username, password=password)
