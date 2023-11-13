from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.capacities import capacity_create_request


def test_create_min_capacity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a min capacity time series.
    """
    create_request = capacity_create_request("min", db, normal_user_headers)
    response = client.post("/min-capacities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["min_capacity"] == create_request.min_capacity
