import random
import string

from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.api.deps import get_current_user
from ensysmod.database.base_class import Base
from ensysmod.model import User
from ensysmod.schemas import UserCreate, UserUpdate


def random_lower_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_float_numbers(size: int = 10) -> list[float]:
    return [random.uniform(0, 1) for _ in range(size)]


def user_authentication_headers(*, client: TestClient, username: str, password: str) -> dict[str, str]:
    data = {"username": username, "password": password}

    r = client.post("/auth/login", data=data, headers={"content-type": "application/x-www-form-urlencoded"})
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    user_in = UserCreate(
        username=random_lower_string(),
        password=random_lower_string(),
    )
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_username(*, client: TestClient, username: str, db: Session) -> dict[str, str]:
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


def get_current_user_from_headers(db: Session, headers: dict[str, str]) -> User:
    token = headers["Authorization"].split()[1]
    return get_current_user(db=db, token=token)


def clear_database(db: Session):
    """
    Clear entries in the database but keep the database structure intact.
    """
    for table in Base.metadata.sorted_tables:
        if table.name != "user":
            db.execute(delete(table))


def clear_users_except_current_user(db: Session, current_user_header: dict[str, str]):
    """
    Delete all users except the current user.
    """
    current_user = get_current_user_from_headers(db, current_user_header)
    db.execute(delete(User).where(User.id != current_user.id))
