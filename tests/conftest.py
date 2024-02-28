from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.app import app
from ensysmod.database.session import SessionLocal
from tests.utils.data_generator.users import generate_credentials, new_user


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
    credentials = generate_credentials()
    if crud.user.get_by_username(db, username=credentials["username"]) is None:
        new_user(db, **credentials)
    return {"Authorization": f"Bearer {crud.user.authenticate(db, **credentials).access_token}"}
