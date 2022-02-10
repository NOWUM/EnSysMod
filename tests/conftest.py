from typing import Generator

import pytest
from fastapi.testclient import TestClient

from ensysmod import crud
from ensysmod.app import app
from ensysmod.database.session import SessionLocal
from tests.utils.utils import authentication_token_from_username, create_random_user


@pytest.fixture(scope="function")
def db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def normal_user_headers(client: TestClient) -> Generator:
    db = SessionLocal()
    user = crud.user.get(db, id=1)
    if user is None:
        user = create_random_user(db)
    yield authentication_token_from_username(db=db, client=client, username=user.username)
