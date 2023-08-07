from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import data_generator


def test_create_fix_capacity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a fix capacity time series.
    """
    create_request = data_generator.get_random_fix_capacity_create(db)
    response = client.post("/fix-capacities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["fix_capacities"] == create_request.fix_capacities
