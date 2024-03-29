from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import CAPACITY_FIX
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_sources import new_source
from tests.utils.data_generator.excel_files import excel_file_type_create_request, generate_excel_file, new_excel_file_type
from tests.utils.data_generator.regions import new_region
from tests.utils.utils import assert_response


def test_get_capacity_fix(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a CapacityFix by its id.
    """
    capacity_fix = new_excel_file_type(CAPACITY_FIX, db, user_header)
    entry_id = capacity_fix.id

    response = client.get(f"/fix-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), capacity_fix)


def test_get_capacity_fix_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a CapacityFix by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(f"/fix-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix {entry_id} not found!"


def test_get_capacity_fix_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityFix of a dataset.
    """
    capacity_fix = new_excel_file_type(CAPACITY_FIX, db, user_header)
    dataset_id = capacity_fix.ref_dataset

    response = client.get(f"/fix-capacities/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json()[0], capacity_fix)


def test_get_capacity_fix_by_dataset_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityFix of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(f"/fix-capacities/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix for dataset {dataset_id} not found!"


def test_get_capacity_fix_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityFix of a component.
    """
    capacity_fix = new_excel_file_type(CAPACITY_FIX, db, user_header)
    component_id = capacity_fix.ref_component

    response = client.get(f"/fix-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json()[0], capacity_fix)


def test_get_capacity_fix_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/fix-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix for component {component_id} not found!"


def test_create_capacity_fix(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityFix.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, user_header)

    response = client.post("/fix-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_capacity_fix_dataset_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityFix, with invalid ref_dataset.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, user_header)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/fix-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Dataset {create_request.ref_dataset} not found!"


def test_create_capacity_fix_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityFix, with invalid component name.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, user_header)
    create_request.component_name = "Invalid component name"  # invalid

    response = client.post("/fix-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {create_request.component_name} not found in dataset {create_request.ref_dataset}!"


def test_create_capacity_fix_region_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityFix, with invalid region name.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, user_header)
    create_request.region_name = "Invalid region name"  # invalid

    response = client.post("/fix-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region_name} not found in dataset {create_request.ref_dataset}!"


def test_create_existing_capacity_fix(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a CapacityFix that already exists.
    """
    create_request = excel_file_type_create_request(CAPACITY_FIX, db, user_header)

    response = client.post("/fix-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/fix-capacities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_capacity_fix(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a CapacityFix.
    """
    capacity_fix = new_excel_file_type(CAPACITY_FIX, db, user_header)
    entry_id = capacity_fix.id

    response = client.delete(f"/fix-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), capacity_fix)


def test_remove_capacity_fix_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a CapacityFix, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/fix-capacities/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix {entry_id} not found!"


def test_remove_capacity_fix_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all CapacityFix of a component.
    """
    capacity_fix = new_excel_file_type(CAPACITY_FIX, db, user_header)
    component_id = capacity_fix.ref_component

    response = client.delete(f"/fix-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json()[0], capacity_fix)


def test_remove_capacity_fix_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/fix-capacities/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"CapacityFix for component {component_id} not found!"


def test_upload_capacity_fix(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading CapacityFix of a component.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=1) as file:
        response = client.post(
            f"/fix-capacities/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_200_OK

        uploaded_file = response.json()
        assert uploaded_file["file"] == file.name
        assert uploaded_file["status"] == "OK"


def test_upload_capacity_fix_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    with generate_excel_file(region_names=["region"], length=1) as file:
        response = client.post(
            f"/fix-capacities/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        error_detail = response.json()["detail"]
        assert error_detail == f"Component {component_id} not found!"


def test_upload_capacity_fix_bad_request(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading CapacityFix of a component, with an incorrect length of data.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=2) as file:  # length should be 1
        response = client.post(
            f"/fix-capacities/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_detail = response.json()["detail"]
        assert error_detail["file"] == file.name
        assert error_detail["status"] == "ERROR"


def test_download_capacity_fix(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading CapacityFix of a component.
    """
    capacity_fix = new_excel_file_type(CAPACITY_FIX, db, user_header)
    component_id = capacity_fix.ref_component

    response = client.get(f"/fix-capacities/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_capacity_fix_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading CapacityFix of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/fix-capacities/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {component_id} not found!"
