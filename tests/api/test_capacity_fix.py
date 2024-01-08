from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import CAPACITY_FIX
from tests.utils.assertions import assert_excel_file_entry
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.excel_files import (
    excel_file_type_create,
    excel_file_type_create_request,
    generate_excel_file,
)
from tests.utils.data_generator.regions import region_create


def test_get_capacity_fix(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a CapacityFix by its id.
    """
    capacity_fix = excel_file_type_create(CAPACITY_FIX, db, normal_user_headers)
    entry_id = capacity_fix.id

    response = client.get(
        f"/fix-capacities/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()
    assert_excel_file_entry(entry=retrieved_entry, expected=capacity_fix, data_column="capacity_fix")


def test_get_capacity_fix_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a CapacityFix by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(
        f"/fix-capacities/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix {entry_id} not found!"


def test_get_capacity_fix_by_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all CapacityFix of a dataset.
    """
    capacity_fix = excel_file_type_create(CAPACITY_FIX, db, normal_user_headers)
    dataset_id = capacity_fix.ref_dataset

    response = client.get(
        f"/fix-capacities/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=capacity_fix, data_column="capacity_fix")


def test_get_capacity_fix_by_dataset_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all CapacityFix of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(
        f"/fix-capacities/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix for dataset {dataset_id} not found!"


def test_get_capacity_fix_by_component(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all CapacityFix of a component.
    """
    capacity_fix = excel_file_type_create(CAPACITY_FIX, db, normal_user_headers)
    component_id = capacity_fix.ref_component

    response = client.get(
        f"/fix-capacities/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=capacity_fix, data_column="capacity_fix")


def test_get_capacity_fix_by_component_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/fix-capacities/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix for component {component_id} not found!"


def test_create_capacity_fix(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a CapacityFix.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, normal_user_headers)

    response = client.post("/fix-capacities/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_entry = response.json()
    assert created_entry["dataset"]["id"] == create_request.ref_dataset
    assert created_entry["component"]["name"] == create_request.component
    assert created_entry["region"]["name"] == create_request.region
    assert created_entry["capacity_fix"] == create_request.capacity_fix


def test_create_capacity_fix_dataset_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a CapacityFix, with invalid ref_dataset.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, normal_user_headers)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/fix-capacities/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Dataset {create_request.ref_dataset} not found!"


def test_create_capacity_fix_component_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a CapacityFix, with invalid component name.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, normal_user_headers)
    create_request.component = "Invalid component name"  # invalid

    response = client.post("/fix-capacities/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {create_request.component} not found in dataset {create_request.ref_dataset}!"


def test_create_capacity_fix_region_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a CapacityFix, with invalid region name.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, normal_user_headers)
    create_request.region = "Invalid region name"  # invalid

    response = client.post("/fix-capacities/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region} not found in dataset {create_request.ref_dataset}!"


def test_create_existing_capacity_fix(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a CapacityFix that already exists.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, normal_user_headers)

    response = client.post("/fix-capacities/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/fix-capacities/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_capacity_fix(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a CapacityFix.
    """
    capacity_fix = excel_file_type_create(CAPACITY_FIX, db, normal_user_headers)
    entry_id = capacity_fix.id

    response = client.delete(f"/fix-capacities/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()
    assert deleted_entry["id"] == entry_id


def test_remove_capacity_fix_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a CapacityFix, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/fix-capacities/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix {entry_id} not found!"


def test_remove_capacity_fix_by_component(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all CapacityFix of a component.
    """
    capacity_fix = excel_file_type_create(CAPACITY_FIX, db, normal_user_headers)
    component_id = capacity_fix.ref_component

    response = client.delete(f"/fix-capacities/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()[0]
    assert deleted_entry["component"]["id"] == component_id


def test_remove_capacity_fix_by_component_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/fix-capacities/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix for component {component_id} not found!"


def test_upload_capacity_fix(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading CapacityFix of a component.
    """
    dataset = dataset_create(db, normal_user_headers)
    component = source_create(db, normal_user_headers, dataset_id=dataset.id)
    component_id = component.component.id
    region = region_create(db, normal_user_headers, dataset_id=dataset.id)
    region2 = region_create(db, normal_user_headers, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=1) as file:
        response = client.post(
            f"/fix-capacities/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_200_OK

        uploaded_file = response.json()
        assert uploaded_file["file"] == file.name
        assert uploaded_file["status"] == "OK"


def test_upload_capacity_fix_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    with generate_excel_file(region_names=["region"], length=1) as file:
        response = client.post(
            f"/fix-capacities/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        error_detail = response.json()["detail"]
        assert error_detail == f"Component {component_id} not found!"


def test_upload_capacity_fix_bad_request(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading CapacityFix of a component, with an incorrect length of data.
    """
    dataset = dataset_create(db, normal_user_headers)
    component = source_create(db, normal_user_headers, dataset_id=dataset.id)
    component_id = component.component.id
    region = region_create(db, normal_user_headers, dataset_id=dataset.id)
    region2 = region_create(db, normal_user_headers, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=2) as file:  # length should be 1
        response = client.post(
            f"/fix-capacities/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_detail = response.json()["detail"]
        assert error_detail["file"] == file.name
        assert error_detail["status"] == "ERROR"


def test_download_capacity_fix(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading CapacityFix of a component.
    """
    capacity_fix = excel_file_type_create(CAPACITY_FIX, db, normal_user_headers)
    component_id = capacity_fix.ref_component

    response = client.get(
        f"/fix-capacities/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_capacity_fix_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/fix-capacities/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {component_id} not found!"
