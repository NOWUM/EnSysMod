from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import TRANSMISSION_DISTANCE
from tests.utils.assertions import assert_excel_file_entry
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_sources import new_source
from tests.utils.data_generator.excel_files import excel_file_type_create_request, generate_excel_file, new_excel_file_type
from tests.utils.data_generator.regions import new_region


def test_get_transmission_distance(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a TransmissionDistance by its id.
    """
    transmission_distance = new_excel_file_type(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    entry_id = transmission_distance.id

    response = client.get(f"/transmission-distances/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()
    assert_excel_file_entry(entry=retrieved_entry, expected=transmission_distance, data_column="distance")


def test_get_transmission_distance_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting a TransmissionDistance by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(f"/transmission-distances/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionDistance {entry_id} not found!"


def test_get_transmission_distance_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all TransmissionDistance of a dataset.
    """
    transmission_distance = new_excel_file_type(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    dataset_id = transmission_distance.ref_dataset

    response = client.get(f"/transmission-distances/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=transmission_distance, data_column="distance")


def test_get_transmission_distance_by_dataset_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all TransmissionDistance of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(f"/transmission-distances/dataset/{dataset_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionDistance for dataset {dataset_id} not found!"


def test_get_transmission_distance_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all TransmissionDistance of a component.
    """
    transmission_distance = new_excel_file_type(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    component_id = transmission_distance.ref_component

    response = client.get(f"/transmission-distances/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=transmission_distance, data_column="distance")


def test_get_transmission_distance_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all TransmissionDistance of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/transmission-distances/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionDistance for component {component_id} not found!"


def test_create_transmission_distance(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a TransmissionDistance.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)

    response = client.post("/transmission-distances/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK

    created_entry = response.json()
    assert created_entry["dataset"]["id"] == create_request.ref_dataset
    assert created_entry["component"]["name"] == create_request.component
    assert created_entry["region"]["name"] == create_request.region
    assert created_entry["region_to"]["name"] == create_request.region_to
    assert created_entry["distance"] == create_request.distance


def test_create_transmission_distance_dataset_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a TransmissionDistance, with invalid ref_dataset.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/transmission-distances/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Dataset {create_request.ref_dataset} not found!"


def test_create_transmission_distance_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a TransmissionDistance, with invalid component name.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    create_request.component = "Invalid component name"  # invalid

    response = client.post("/transmission-distances/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {create_request.component} not found in dataset {create_request.ref_dataset}!"


def test_create_transmission_distance_region_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a TransmissionDistance, with invalid region name.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    create_request.region = "Invalid region name"  # invalid

    response = client.post("/transmission-distances/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region} not found in dataset {create_request.ref_dataset}!"


def test_create_transmission_distance_region_to_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a TransmissionDistance, with invalid region_to name.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    create_request.region_to = "Invalid region_to name"  # invalid

    response = client.post("/transmission-distances/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region_to} not found in dataset {create_request.ref_dataset}!"


def test_create_existing_transmission_distance(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a TransmissionDistance that already exists.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)

    response = client.post("/transmission-distances/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/transmission-distances/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_transmission_distance(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a TransmissionDistance.
    """
    transmission_distance = new_excel_file_type(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    entry_id = transmission_distance.id

    response = client.delete(f"/transmission-distances/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()
    assert deleted_entry["id"] == entry_id


def test_remove_transmission_distance_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing a TransmissionDistance, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/transmission-distances/{entry_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionDistance {entry_id} not found!"


def test_remove_transmission_distance_by_component(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all TransmissionDistance of a component.
    """
    transmission_distance = new_excel_file_type(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    component_id = transmission_distance.ref_component

    response = client.delete(f"/transmission-distances/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()[0]
    assert deleted_entry["component"]["id"] == component_id


def test_remove_transmission_distance_by_component_entry_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test removing all TransmissionDistance of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/transmission-distances/component/{component_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionDistance for component {component_id} not found!"


def test_upload_transmission_distance(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading TransmissionDistance of a component.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], as_matrix=True) as file:
        response = client.post(
            f"/transmission-distances/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_200_OK

        uploaded_file = response.json()
        assert uploaded_file["file"] == file.name
        assert uploaded_file["status"] == "OK"


def test_upload_transmission_distance_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading TransmissionDistance of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    with generate_excel_file(region_names=["region"], as_matrix=True) as file:
        response = client.post(
            f"/transmission-distances/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        error_detail = response.json()["detail"]
        assert error_detail == f"Component {component_id} not found!"


def test_upload_transmission_distance_bad_request(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test uploading TransmissionDistance of a component, with an unknown region in the data.
    """
    dataset = new_dataset(db, user_header)
    component = new_source(db, user_header, dataset_id=dataset.id)
    component_id = component.component.id
    region = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name, "unknown region"], as_matrix=True) as file:  # unknown region doesn't exist
        response = client.post(
            f"/transmission-distances/component/{component_id}/upload",
            headers=user_header,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_detail = response.json()["detail"]
        assert error_detail["file"] == file.name
        assert error_detail["status"] == "ERROR"


def test_download_transmission_distance(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading TransmissionDistance of a component.
    """
    transmission_distance = new_excel_file_type(TRANSMISSION_DISTANCE, db, user_header, transmission_component=True)
    component_id = transmission_distance.ref_component

    response = client.get(f"/transmission-distances/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_transmission_distance_component_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test downloading TransmissionDistance of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(f"/transmission-distances/component/{component_id}/download", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {component_id} not found!"
