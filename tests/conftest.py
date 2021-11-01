from typing import Generator

import pytest
from fastapi.testclient import TestClient

from counter.app import app
from counter.database.session import SessionLocal


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
