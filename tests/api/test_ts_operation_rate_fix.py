from pathlib import Path

from fastapi import status
from fastapi.testclient import TestClient
from schemas.region import RegionCreate
from sqlalchemy.orm import Session

from ensysmod import crud
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.operation_rates import operation_rate_create, operation_rate_create_request
from tests.utils.utils import get_project_root


def test_create_fix_operation_rate(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix operation rate time series.
    """
    create_request = operation_rate_create_request("fix", db, normal_user_headers)
    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["fix_operation_rates"] == create_request.fix_operation_rates


def test_upload_fix_operation_rate(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading a fix operation rate excel file.
    """
    component = source_create(db, normal_user_headers)
    component_id = component.component.id

    # Region name must match the column name in the excel file.
    crud.region.create(db=db, obj_in=RegionCreate(name="GermanyRegion", ref_dataset=component.component.ref_dataset))
    # TODO generate random values in a temporary file instead of using excel file from the example dataset
    file_path = Path(get_project_root(), "examples/datasets/1node_Example/sources/Wind (onshore)/operationRateMax.xlsx")

    response = client.post(
        f"/fix-operation-rates/component/{component_id}/upload",
        headers=normal_user_headers,
        files={"file": ("operationRateFix.xlsx", file_path.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert response.status_code == status.HTTP_200_OK

    uploaded_file = response.json()
    assert uploaded_file["status"] == "OK"


def test_download_fix_operation_rate(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading a fix operation rate excel file.
    """
    operation_rate_fix = operation_rate_create("fix", db, normal_user_headers)
    component_id = operation_rate_fix.ref_component

    response = client.get(
        f"/fix-operation-rates/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
