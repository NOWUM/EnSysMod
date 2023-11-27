from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.operation_rates import generate_time_series_excel_file, operation_rate_create, operation_rate_create_request
from tests.utils.data_generator.regions import region_create


def test_get_fix_operation_rate(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a fix operation rate by its id.
    """
    operation_rate_fix = operation_rate_create("fix", db, normal_user_headers)
    entry_id = operation_rate_fix.id

    response = client.get(
        f"/fix-operation-rates/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()
    assert retrieved_entry["id"] == operation_rate_fix.id
    assert retrieved_entry["dataset"]["id"] == operation_rate_fix.ref_dataset
    assert retrieved_entry["component"]["name"] == operation_rate_fix.component.name
    assert retrieved_entry["region"]["name"] == operation_rate_fix.region.name
    assert retrieved_entry["fix_operation_rates"] == operation_rate_fix.fix_operation_rates


def test_get_fix_operation_rate_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a fix operation rate by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(
        f"/fix-operation-rates/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Fix operation rate {entry_id} not found!"


def test_get_fix_operation_rate_by_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all fix operation rates of a dataset.
    """
    operation_rate_fix = operation_rate_create("fix", db, normal_user_headers)
    dataset_id = operation_rate_fix.ref_dataset

    response = client.get(
        f"/fix-operation-rates/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert retrieved_entry["id"] == operation_rate_fix.id
    assert retrieved_entry["dataset"]["id"] == operation_rate_fix.ref_dataset
    assert retrieved_entry["component"]["name"] == operation_rate_fix.component.name
    assert retrieved_entry["region"]["name"] == operation_rate_fix.region.name
    assert retrieved_entry["fix_operation_rates"] == operation_rate_fix.fix_operation_rates


def test_get_fix_operation_rate_by_dataset_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all fix operation rates of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(
        f"/fix-operation-rates/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Fix operation rate for dataset {dataset_id} not found!"


def test_get_fix_operation_rate_by_component(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all fix operation rates of a component.
    """
    operation_rate_fix = operation_rate_create("fix", db, normal_user_headers)
    component_id = operation_rate_fix.ref_component

    response = client.get(
        f"/fix-operation-rates/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert retrieved_entry["id"] == operation_rate_fix.id
    assert retrieved_entry["dataset"]["id"] == operation_rate_fix.ref_dataset
    assert retrieved_entry["component"]["name"] == operation_rate_fix.component.name
    assert retrieved_entry["region"]["name"] == operation_rate_fix.region.name
    assert retrieved_entry["fix_operation_rates"] == operation_rate_fix.fix_operation_rates


def test_get_fix_operation_rate_by_component_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all fix operation rates of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/fix-operation-rates/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Fix operation rate for component {component_id} not found!"


def test_create_fix_operation_rate(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix operation rate time series.
    """
    create_request = operation_rate_create_request("fix", db, normal_user_headers)

    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_entry = response.json()
    assert created_entry["dataset"]["id"] == create_request.ref_dataset
    assert created_entry["component"]["name"] == create_request.component
    assert created_entry["region"]["name"] == create_request.region
    assert created_entry["fix_operation_rates"] == create_request.fix_operation_rates


def test_create_fix_operation_rate_dataset_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix operation rate time series, with invalid ref_dataset.
    """
    create_request = operation_rate_create_request("fix", db, normal_user_headers)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Dataset {create_request.ref_dataset} not found!"


def test_create_fix_operation_rate_component_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix operation rate time series, with invalid component name.
    """
    create_request = operation_rate_create_request("fix", db, normal_user_headers)
    create_request.component = "Invalid component name"  # invalid

    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Component {create_request.component} not found in dataset {create_request.ref_dataset}!"


def test_create_fix_operation_rate_region_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix operation rate time series, with invalid region name.
    """
    create_request = operation_rate_create_request("fix", db, normal_user_headers)
    create_request.region = "Invalid region name"  # invalid

    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Region {create_request.region} not found in dataset {create_request.ref_dataset}!"


def test_create_fix_operation_rate_invalid_length(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix operation rate time series, with invalid length of time series data.
    """
    create_request = operation_rate_create_request("fix", db, normal_user_headers)
    create_request.fix_operation_rates.append(0)  # add one more value to the time series data

    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_existing_fix_operation_rate(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a fix operation rate time series that already exists.
    """
    create_request = operation_rate_create_request("fix", db, normal_user_headers)

    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_fix_operation_rate(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a fix operation rate.
    """
    operation_rate_fix = operation_rate_create("fix", db, normal_user_headers)
    entry_id = operation_rate_fix.id

    response = client.delete(f"/fix-operation-rates/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()
    assert deleted_entry["id"] == entry_id


def test_remove_fix_operation_rate_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a fix operation rate, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/fix-operation-rates/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Fix operation rate {entry_id} not found!"


def test_remove_fix_operation_rate_by_component(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all fix operation rates of a component.
    """
    operation_rate_fix = operation_rate_create("fix", db, normal_user_headers)
    component_id = operation_rate_fix.ref_component

    response = client.delete(f"/fix-operation-rates/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()[0]
    assert deleted_entry["component"]["id"] == component_id


def test_remove_fix_operation_rate_by_component_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all fix operation rates of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/fix-operation-rates/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Fix operation rate for component {component_id} not found!"


def test_upload_fix_operation_rate(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading fix operation rates of a component.
    """
    dataset = dataset_create(db, normal_user_headers)
    component = source_create(db, normal_user_headers, dataset_id=dataset.id)
    component_id = component.component.id
    region = region_create(db, normal_user_headers, dataset_id=dataset.id)

    file = generate_time_series_excel_file(region_names=[region.name])

    response = client.post(
        f"/fix-operation-rates/component/{component_id}/upload",
        headers=normal_user_headers,
        files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert response.status_code == status.HTTP_200_OK

    uploaded_file = response.json()
    assert uploaded_file["file"] == file.name
    assert uploaded_file["status"] == "OK"


def test_upload_fix_operation_rate_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading fix operation rates of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    file = generate_time_series_excel_file(region_names=["region"], length=1)

    response = client.post(
        f"/fix-operation-rates/component/{component_id}/upload",
        headers=normal_user_headers,
        files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Component {component_id} not found!"


def test_download_fix_operation_rate(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading fix operation rates of a component.
    """
    operation_rate_fix = operation_rate_create("fix", db, normal_user_headers)
    component_id = operation_rate_fix.ref_component

    response = client.get(
        f"/fix-operation-rates/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_fix_operation_rate_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading fix operation rates of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/fix-operation-rates/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Component {component_id} not found!"
