from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import YEARLY_FULL_LOAD_HOURS_MAX
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_sources import new_source
from tests.utils.data_generator.excel_files import excel_file_type_create_request, generate_excel_file, new_excel_file_type
from tests.utils.data_generator.regions import new_region
from tests.utils.utils import assert_response


def test_get_yearly_full_load_hours_max(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a YearlyFullLoadHoursMax by its id.
    """
    yearly_full_load_hours_max = new_excel_file_type(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    entry_id = yearly_full_load_hours_max.id

    response = client.get(f"/max-yearly-full-load-hours/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), yearly_full_load_hours_max)


def test_get_yearly_full_load_hours_max_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a YearlyFullLoadHoursMax by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(f"/max-yearly-full-load-hours/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMax {entry_id} not found!"


def test_get_yearly_full_load_hours_max_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMax of a dataset.
    """
    yearly_full_load_hours_max = new_excel_file_type(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    dataset_id = yearly_full_load_hours_max.ref_dataset

    response = client.get(f"/max-yearly-full-load-hours/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json()[0], yearly_full_load_hours_max)


def test_get_yearly_full_load_hours_max_by_dataset_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMax of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(f"/max-yearly-full-load-hours/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMax for dataset {dataset_id} not found!"


def test_get_yearly_full_load_hours_max_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMax of a component.
    """
    yearly_full_load_hours_max = new_excel_file_type(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    component_id = yearly_full_load_hours_max.ref_component

    response = client.get(f"/max-yearly-full-load-hours/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json()[0], yearly_full_load_hours_max)


def test_get_yearly_full_load_hours_max_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all YearlyFullLoadHoursMax of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/max-yearly-full-load-hours/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMax for component {component_id} not found!"


def test_create_yearly_full_load_hours_max(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMax.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)

    response = client.post("/max-yearly-full-load-hours/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_yearly_full_load_hours_max_dataset_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMax, with invalid ref_dataset.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/max-yearly-full-load-hours/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Dataset {create_request.ref_dataset} not found!"


def test_create_yearly_full_load_hours_max_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMax, with invalid component name.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    create_request.component_name = "Invalid component name"  # invalid

    response = client.post("/max-yearly-full-load-hours/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {create_request.component_name} not found in dataset {create_request.ref_dataset}!"


def test_create_yearly_full_load_hours_max_region_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMax, with invalid region name.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    create_request.region_name = "Invalid region name"  # invalid

    response = client.post("/max-yearly-full-load-hours/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region_name} not found in dataset {create_request.ref_dataset}!"


def test_create_existing_yearly_full_load_hours_max(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a YearlyFullLoadHoursMax that already exists.
    """
    create_request = excel_file_type_create_request(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)

    response = client.post("/max-yearly-full-load-hours/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/max-yearly-full-load-hours/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_yearly_full_load_hours_max(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a YearlyFullLoadHoursMax.
    """
    yearly_full_load_hours_max = new_excel_file_type(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    entry_id = yearly_full_load_hours_max.id

    response = client.delete(f"/max-yearly-full-load-hours/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), yearly_full_load_hours_max)


def test_remove_yearly_full_load_hours_max_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a YearlyFullLoadHoursMax, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/max-yearly-full-load-hours/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMax {entry_id} not found!"


def test_remove_yearly_full_load_hours_max_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all YearlyFullLoadHoursMax of a component.
    """
    yearly_full_load_hours_max = new_excel_file_type(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    component_id = yearly_full_load_hours_max.ref_component

    response = client.delete(f"/max-yearly-full-load-hours/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json()[0], yearly_full_load_hours_max)


def test_remove_yearly_full_load_hours_max_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all YearlyFullLoadHoursMax of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/max-yearly-full-load-hours/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"YearlyFullLoadHoursMax for component {component_id} not found!"


def test_upload_yearly_full_load_hours_max(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading YearlyFullLoadHoursMax of a component.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=1) as file:
        response = client.post(
            f"/max-yearly-full-load-hours/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_200_OK

        uploaded_file = response.json()
        assert uploaded_file["file"] == file.name
        assert uploaded_file["status"] == "OK"


def test_upload_yearly_full_load_hours_max_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading YearlyFullLoadHoursMax of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    with generate_excel_file(region_names=["region"], length=1) as file:
        response = client.post(
            f"/max-yearly-full-load-hours/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        error_detail = response.json()["detail"]
        assert error_detail == f"Component {component_id} not found!"


def test_upload_yearly_full_load_hours_max_bad_request(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading YearlyFullLoadHoursMax of a component, with an incorrect length of data.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], length=2) as file:  # length should be 1
        response = client.post(
            f"/max-yearly-full-load-hours/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_detail = response.json()["detail"]
        assert error_detail["file"] == file.name
        assert error_detail["status"] == "ERROR"


def test_download_yearly_full_load_hours_max(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading YearlyFullLoadHoursMax of a component.
    """
    yearly_full_load_hours_max = new_excel_file_type(YEARLY_FULL_LOAD_HOURS_MAX, db, user_header)
    component_id = yearly_full_load_hours_max.ref_component

    response = client.get(f"/max-yearly-full-load-hours/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_yearly_full_load_hours_max_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading YearlyFullLoadHoursMax of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/max-yearly-full-load-hours/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {component_id} not found!"
