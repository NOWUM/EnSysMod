from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
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
    assert r2.status_code == status.HTTP_409_CONFLICT


def test_login_endpoint(client: TestClient, db: Session):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    assert r.status_code == status.HTTP_200_OK

    r2 = client.post("/auth/login", data=payload, headers={"content-type": "application/x-www-form-urlencoded"})
    assert r2.status_code == status.HTTP_200_OK
    assert r2.json()['access_token']
    assert r2.json()['token_type'] == 'bearer'


def test_login_unknown_user_endpoint(client: TestClient, db: Session):
    payload = get_register_payload()
    r = client.post("/auth/login", data=payload, headers={"content-type": "application/x-www-form-urlencoded"})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_token_endpoint(client: TestClient):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    assert r.status_code == status.HTTP_200_OK

    r2 = client.post("/auth/login", data=payload, headers={"content-type": "application/x-www-form-urlencoded"})
    assert r2.status_code == status.HTTP_200_OK

    r3 = client.get("/auth/test-token", headers={"Authorization": f"Bearer {r2.json()['access_token']}"})
    user = r3.json()
    assert r3.status_code == status.HTTP_200_OK
    assert user['username'] == payload['username']


def test_test_token_unknown_access_token_endpoint(client: TestClient):
    r = client.get("/auth/test-token", headers={"Authorization": "Bearer unknown"})
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_test_token_user_deleted(client: TestClient, db: Session):
    payload = get_register_payload()
    r = client.post("/auth/register", json=payload)
    assert r.status_code == status.HTTP_200_OK

    r2 = client.post("/auth/login", data=payload, headers={"content-type": "application/x-www-form-urlencoded"})
    assert r2.status_code == status.HTTP_200_OK

    user_id = crud.user.get_by_username(db=db, username=payload['username']).id
    crud.user.remove(db=db, id=user_id)

    r3 = client.get("/auth/test-token", headers={"Authorization": f"Bearer {r2.json()['access_token']}"})
    assert r3.status_code == status.HTTP_401_UNAUTHORIZED
