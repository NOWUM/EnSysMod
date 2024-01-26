from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.app import app
from ensysmod.database.session import SessionLocal
from ensysmod.schemas import UserCreate
from tests.utils.utils import random_string


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def user_header(db: Session) -> dict[str, str]:
    """
    Return a valid user header.
    If the user doesn't exist it is created first.
    """
    data = {"username": random_string(), "password": random_string()}
    if crud.user.get_by_username(db, username=data["username"]) is None:
        crud.user.create(db, obj_in=UserCreate(**data))
    return {"Authorization": f"Bearer {crud.user.authenticate(db, **data).access_token}"}
