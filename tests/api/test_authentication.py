from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from counter import crud
from tests.utils.utils import random_lower_string


def get_register_payload():
    return {"username": random_lower_string(), "password": random_lower_string()}


def test_register_endpoint(client: TestClient, db: Session):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    new_user = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert new_user
    assert new_user['username'] == payload['username']
    db_user = crud.user.get_by_username(db=db, username=payload['username'])
    assert db_user


def test_register_twice_endpoint(client: TestClient):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    new_user = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert new_user
    assert new_user['username'] == payload['username']

    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == status.HTTP_400_BAD_REQUEST
