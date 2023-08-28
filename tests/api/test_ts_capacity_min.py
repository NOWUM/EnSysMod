from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import data_generator


def test_create_min_capacity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a min capacity time series.
    """
    create_request = data_generator.get_random_min_capacity_create(db)
    response = client.post("/min-capacities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["min_capacities"] == create_request.min_capacities
