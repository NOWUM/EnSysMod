from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import CAPACITY_FIX
from tests.utils.data_generator.excel_files import excel_file_type_create_request


def test_create_fix_capacity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix capacity time series.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, normal_user_headers)
    response = client.post("/fix-capacities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["fix_capacity"] == create_request.fix_capacity
