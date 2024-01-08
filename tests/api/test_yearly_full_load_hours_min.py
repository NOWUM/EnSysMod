from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import YEARLY_FULL_LOAD_HOURS_MIN
from tests.utils.assertions import assert_excel_file_entry
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.excel_files import (
    excel_file_type_create,
    excel_file_type_create_request,
    generate_excel_file,
)
from tests.utils.data_generator.regions import region_create


def test_get_yearly_full_load_hours_min(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a YearlyFullLoadHoursMin by its id.
    """
    yearly_full_load_hours_min = excel_file_type_create(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    entry_id = yearly_full_load_hours_min.id

    response = client.get(
        f"/min-yearly-full-load-hours/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()
    assert_excel_file_entry(entry=retrieved_entry, expected=yearly_full_load_hours_min, data_column="yearly_full_load_hours_min")


def test_get_yearly_full_load_hours_min_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a YearlyFullLoadHoursMin by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(
        f"/min-yearly-full-load-hours/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMin {entry_id} not found!"


def test_get_yearly_full_load_hours_min_by_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMin of a dataset.
    """
    yearly_full_load_hours_min = excel_file_type_create(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    dataset_id = yearly_full_load_hours_min.ref_dataset

    response = client.get(
        f"/min-yearly-full-load-hours/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=yearly_full_load_hours_min, data_column="yearly_full_load_hours_min")


def test_get_yearly_full_load_hours_min_by_dataset_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMin of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(
        f"/min-yearly-full-load-hours/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMin for dataset {dataset_id} not found!"


def test_get_yearly_full_load_hours_min_by_component(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMin of a component.
    """
    yearly_full_load_hours_min = excel_file_type_create(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    component_id = yearly_full_load_hours_min.ref_component

    response = client.get(
        f"/min-yearly-full-load-hours/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=yearly_full_load_hours_min, data_column="yearly_full_load_hours_min")


def test_get_yearly_full_load_hours_min_by_component_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/min-yearly-full-load-hours/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMin for component {component_id} not found!"


def test_create_yearly_full_load_hours_min(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMin.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)

    response = client.post("/min-yearly-full-load-hours/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_entry = response.json()
    assert created_entry["dataset"]["id"] == create_request.ref_dataset
    assert created_entry["component"]["name"] == create_request.component
    assert created_entry["region"]["name"] == create_request.region
    assert created_entry["yearly_full_load_hours_min"] == create_request.yearly_full_load_hours_min


def test_create_yearly_full_load_hours_min_dataset_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMin, with invalid ref_dataset.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/min-yearly-full-load-hours/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Dataset {create_request.ref_dataset} not found!"


def test_create_yearly_full_load_hours_min_component_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMin, with invalid component name.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    create_request.component = "Invalid component name"  # invalid

    response = client.post("/min-yearly-full-load-hours/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {create_request.component} not found in dataset {create_request.ref_dataset}!"


def test_create_yearly_full_load_hours_min_region_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMin, with invalid region name.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    create_request.region = "Invalid region name"  # invalid

    response = client.post("/min-yearly-full-load-hours/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region} not found in dataset {create_request.ref_dataset}!"


def test_create_existing_yearly_full_load_hours_min(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMin that already exists.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)

    response = client.post("/min-yearly-full-load-hours/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/min-yearly-full-load-hours/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_yearly_full_load_hours_min(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a YearlyFullLoadHoursMin.
    """
    yearly_full_load_hours_min = excel_file_type_create(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    entry_id = yearly_full_load_hours_min.id

    response = client.delete(f"/min-yearly-full-load-hours/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()
    assert deleted_entry["id"] == entry_id


def test_remove_yearly_full_load_hours_min_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a YearlyFullLoadHoursMin, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/min-yearly-full-load-hours/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMin {entry_id} not found!"


def test_remove_yearly_full_load_hours_min_by_component(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all YearlyFullLoadHoursMin of a component.
    """
    yearly_full_load_hours_min = excel_file_type_create(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    component_id = yearly_full_load_hours_min.ref_component

    response = client.delete(f"/min-yearly-full-load-hours/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()[0]
    assert deleted_entry["component"]["id"] == component_id


def test_remove_yearly_full_load_hours_min_by_component_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all YearlyFullLoadHoursMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/min-yearly-full-load-hours/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMin for component {component_id} not found!"


def test_upload_yearly_full_load_hours_min(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading YearlyFullLoadHoursMin of a component.
    """
    dataset = dataset_create(db, normal_user_headers)
    component = source_create(db, normal_user_headers, dataset_id=dataset.id)
    component_id = component.component.id
    region = region_create(db, normal_user_headers, dataset_id=dataset.id)
    region2 = region_create(db, normal_user_headers, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=1) as file:
        response = client.post(
            f"/min-yearly-full-load-hours/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_200_OK

        uploaded_file = response.json()
        assert uploaded_file["file"] == file.name
        assert uploaded_file["status"] == "OK"


def test_upload_yearly_full_load_hours_min_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading YearlyFullLoadHoursMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    with generate_excel_file(region_names=["region"], length=1) as file:
        response = client.post(
            f"/min-yearly-full-load-hours/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        error_detail = response.json()["detail"]
        assert error_detail == f"Component {component_id} not found!"


def test_upload_yearly_full_load_hours_min_bad_request(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading YearlyFullLoadHoursMin of a component, with an incorrect length of data.
    """
    dataset = dataset_create(db, normal_user_headers)
    component = source_create(db, normal_user_headers, dataset_id=dataset.id)
    component_id = component.component.id
    region = region_create(db, normal_user_headers, dataset_id=dataset.id)
    region2 = region_create(db, normal_user_headers, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=2) as file:  # length should be 1
        response = client.post(
            f"/min-yearly-full-load-hours/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_detail = response.json()["detail"]
        assert error_detail["file"] == file.name
        assert error_detail["status"] == "ERROR"


def test_download_yearly_full_load_hours_min(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading YearlyFullLoadHoursMin of a component.
    """
    yearly_full_load_hours_min = excel_file_type_create(YEARLY_FULL_LOAD_HOURS_MIN, db, normal_user_headers)
    component_id = yearly_full_load_hours_min.ref_component

    response = client.get(
        f"/min-yearly-full-load-hours/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_yearly_full_load_hours_min_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading YearlyFullLoadHoursMin of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/min-yearly-full-load-hours/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {component_id} not found!"
