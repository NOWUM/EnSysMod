from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import data_generator


def test_create_fix_operation_rate(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a fix operation rate time series.
    """
    create_request = data_generator.get_random_fix_operation_rate_create(db)
    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["fix_operation_rates"] == create_request.fix_operation_rates
