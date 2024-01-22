from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import CAPACITY_MIN
from tests.utils.assertions import assert_excel_file_entry
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_sources import new_source
from tests.utils.data_generator.excel_files import excel_file_type_create_request, generate_excel_file, new_excel_file_type
from tests.utils.data_generator.regions import new_region


def test_get_capacity_min(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a CapacityMin by its id.
    """
    capacity_min = new_excel_file_type(CAPACITY_MIN, db, user_header)
    entry_id = capacity_min.id

    response = client.get(f"/min-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()
    assert_excel_file_entry(entry=retrieved_entry, expected=capacity_min, data_column="capacity_min")


def test_get_capacity_min_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a CapacityMin by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(f"/min-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityMin {entry_id} not found!"


def test_get_capacity_min_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityMin of a dataset.
    """
    capacity_min = new_excel_file_type(CAPACITY_MIN, db, user_header)
    dataset_id = capacity_min.ref_dataset

    response = client.get(f"/min-capacities/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=capacity_min, data_column="capacity_min")


def test_get_capacity_min_by_dataset_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityMin of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(f"/min-capacities/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityMin for dataset {dataset_id} not found!"


def test_get_capacity_min_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityMin of a component.
    """
    capacity_min = new_excel_file_type(CAPACITY_MIN, db, user_header)
    component_id = capacity_min.ref_component

    response = client.get(f"/min-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=capacity_min, data_column="capacity_min")


def test_get_capacity_min_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/min-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityMin for component {component_id} not found!"


def test_create_capacity_min(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityMin.
    """
    create_request = excel_file_type_create_request(CAPACITY_MIN, db, user_header)

    response = client.post("/min-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK

    created_entry = response.json()
    assert created_entry["dataset"]["id"] == create_request.ref_dataset
    assert created_entry["component"]["name"] == create_request.component
    assert created_entry["region"]["name"] == create_request.region
    assert created_entry["capacity_min"] == create_request.capacity_min


def test_create_capacity_min_dataset_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityMin, with invalid ref_dataset.
    """
    create_request = excel_file_type_create_request(CAPACITY_MIN, db, user_header)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/min-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Dataset {create_request.ref_dataset} not found!"


def test_create_capacity_min_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityMin, with invalid component name.
    """
    create_request = excel_file_type_create_request(CAPACITY_MIN, db, user_header)
    create_request.component = "Invalid component name"  # invalid

    response = client.post("/min-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {create_request.component} not found in dataset {create_request.ref_dataset}!"


def test_create_capacity_min_region_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityMin, with invalid region name.
    """
    create_request = excel_file_type_create_request(CAPACITY_MIN, db, user_header)
    create_request.region = "Invalid region name"  # invalid

    response = client.post("/min-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region} not found in dataset {create_request.ref_dataset}!"


def test_create_existing_capacity_min(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityMin that already exists.
    """
    create_request = excel_file_type_create_request(CAPACITY_MIN, db, user_header)

    response = client.post("/min-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/min-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_capacity_min(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a CapacityMin.
    """
    capacity_min = new_excel_file_type(CAPACITY_MIN, db, user_header)
    entry_id = capacity_min.id

    response = client.delete(f"/min-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()
    assert deleted_entry["id"] == entry_id


def test_remove_capacity_min_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a CapacityMin, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/min-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityMin {entry_id} not found!"


def test_remove_capacity_min_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all CapacityMin of a component.
    """
    capacity_min = new_excel_file_type(CAPACITY_MIN, db, user_header)
    component_id = capacity_min.ref_component

    response = client.delete(f"/min-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()[0]
    assert deleted_entry["component"]["id"] == component_id


def test_remove_capacity_min_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all CapacityMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/min-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityMin for component {component_id} not found!"


def test_upload_capacity_min(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading CapacityMin of a component.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=1) as file:
        response = client.post(
            f"/min-capacities/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_200_OK

        uploaded_file = response.json()
        assert uploaded_file["file"] == file.name
        assert uploaded_file["status"] == "OK"


def test_upload_capacity_min_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading CapacityMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    with generate_excel_file(region_names=["region"], length=1) as file:
        response = client.post(
            f"/min-capacities/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        error_detail = response.json()["detail"]
        assert error_detail == f"Component {component_id} not found!"


def test_upload_capacity_min_bad_request(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading CapacityMin of a component, with an incorrect length of data.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=2) as file:  # length should be 1
        response = client.post(
            f"/min-capacities/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_detail = response.json()["detail"]
        assert error_detail["file"] == file.name
        assert error_detail["status"] == "ERROR"


def test_download_capacity_min(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading CapacityMin of a component.
    """
    capacity_min = new_excel_file_type(CAPACITY_MIN, db, user_header)
    component_id = capacity_min.ref_component

    response = client.get(f"/min-capacities/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_capacity_min_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading CapacityMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/min-capacities/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {component_id} not found!"
