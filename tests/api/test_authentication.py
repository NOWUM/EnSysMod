from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from tests.utils.data_generator.users import generate_credentials, new_user, user_create_request
from tests.utils.utils import assert_response


def test_register_endpoint(client: TestClient):
    create_request = user_create_request()
    response = client.post("/auth/register", content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_register_twice_endpoint(client: TestClient):
    create_request = user_create_request()
    response = client.post("/auth/register", content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/auth/register", content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_login_endpoint(db: Session, client: TestClient):
    credentials = generate_credentials()
    new_user(db, **credentials)

    response = client.post("/auth/login", data=credentials, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_login_unknown_user_endpoint(client: TestClient):
    credentials = generate_credentials()
    response = client.post("/auth/login", data=credentials, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_token_endpoint(db: Session, client: TestClient):
    credentials = generate_credentials()
    user = new_user(db, **credentials)

    response = client.post("/auth/login", data=credentials, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    response = client.get("/auth/test-token", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), user)


def test_test_token_unknown_access_token_endpoint(client: TestClient):
    response = client.get("/auth/test-token", headers={"Authorization": "Bearer unknown"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_test_token_user_deleted(db: Session, client: TestClient):
    credentials = generate_credentials()
    user = new_user(db, **credentials)

    response = client.post("/auth/login", data=credentials, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    crud.user.remove(db=db, id=user.id)

    response = client.get("/auth/test-token", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
