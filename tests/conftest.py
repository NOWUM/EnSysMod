from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from ensysmod import crud
from ensysmod.app import app, init_database
from ensysmod.database.session import SessionLocal
from tests.utils.utils import authentication_token_from_username, create_random_user


@pytest.fixture()
def db() -> Generator:
    init_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        if db is not None:
            db.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def normal_user_headers(client: TestClient) -> dict[str, str]:
    db = SessionLocal()
    user = crud.user.get(db, id=1)
    if user is None:
        user = create_random_user(db)
    return authentication_token_from_username(db=db, client=client, username=user.username)
