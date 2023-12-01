from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import OPERATION_RATE_MAX
from tests.utils.data_generator.excel_files import excel_file_type_create_request


def test_create_max_operation_rate(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a max operation rate time series.
    """
    create_request = excel_file_type_create_request(OPERATION_RATE_MAX,  db, normal_user_headers)
    response = client.post("/max-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["max_operation_rates"] == create_request.max_operation_rates
