from typing import Generator

import pytest
from fastapi.testclient import TestClient

from ensysmod.app import app
from ensysmod.database.session import SessionLocal


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
