from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import TRANSMISSION_LOSS
from tests.utils.assertions import assert_excel_file_entry
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.excel_files import excel_file_type_create, excel_file_type_create_request, generate_excel_file
from tests.utils.data_generator.regions import region_create


def test_get_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a TransmissionLoss by its id.
    """
    transmission_loss = excel_file_type_create(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    entry_id = transmission_loss.id

    response = client.get(
        f"/transmission-losses/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()
    assert_excel_file_entry(entry=retrieved_entry, expected=transmission_loss, data_column="loss")


def test_get_transmission_loss_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting a TransmissionLoss by its id, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.get(
        f"/transmission-losses/{entry_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionLoss {entry_id} not found!"


def test_get_transmission_loss_by_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all TransmissionLoss of a dataset.
    """
    transmission_loss = excel_file_type_create(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    dataset_id = transmission_loss.ref_dataset

    response = client.get(
        f"/transmission-losses/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=transmission_loss, data_column="loss")


def test_get_transmission_loss_by_dataset_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all TransmissionLoss of a dataset, with invalid dataset_id.
    """
    dataset_id = 123456  # invalid

    response = client.get(
        f"/transmission-losses/dataset/{dataset_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionLoss for dataset {dataset_id} not found!"


def test_get_transmission_loss_by_component(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all TransmissionLoss of a component.
    """
    transmission_loss = excel_file_type_create(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    component_id = transmission_loss.ref_component

    response = client.get(
        f"/transmission-losses/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_entry = response.json()[0]
    assert_excel_file_entry(entry=retrieved_entry, expected=transmission_loss, data_column="loss")


def test_get_transmission_loss_by_component_entry_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all TransmissionLoss of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/transmission-losses/component/{component_id}",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionLoss for component {component_id} not found!"


def test_create_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a TransmissionLoss.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)

    response = client.post("/transmission-losses/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_entry = response.json()
    assert created_entry["dataset"]["id"] == create_request.ref_dataset
    assert created_entry["component"]["name"] == create_request.component
    assert created_entry["region"]["name"] == create_request.region
    assert created_entry["region_to"]["name"] == create_request.region_to
    assert created_entry["loss"] == create_request.loss


def test_create_transmission_loss_dataset_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a TransmissionLoss, with invalid ref_dataset.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    create_request.ref_dataset = 123456  # invalid

    response = client.post("/transmission-losses/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Dataset {create_request.ref_dataset} not found!"


def test_create_transmission_loss_component_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a TransmissionLoss, with invalid component name.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    create_request.component = "Invalid component name"  # invalid

    response = client.post("/transmission-losses/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {create_request.component} not found in dataset {create_request.ref_dataset}!"


def test_create_transmission_loss_region_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a TransmissionLoss, with invalid region name.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    create_request.region = "Invalid region name"  # invalid

    response = client.post("/transmission-losses/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region} not found in dataset {create_request.ref_dataset}!"


def test_create_transmission_loss_region_to_not_found(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a TransmissionLoss, with invalid region_to name.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    create_request.region_to = "Invalid region_to name"  # invalid

    response = client.post("/transmission-losses/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Region {create_request.region_to} not found in dataset {create_request.ref_dataset}!"


def test_create_existing_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a TransmissionLoss that already exists.
    """
    create_request = excel_file_type_create_request(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)

    response = client.post("/transmission-losses/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/transmission-losses/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_remove_transmission_loss(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a TransmissionLoss.
    """
    transmission_loss = excel_file_type_create(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    entry_id = transmission_loss.id

    response = client.delete(f"/transmission-losses/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()
    assert deleted_entry["id"] == entry_id


def test_remove_transmission_loss_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing a TransmissionLoss, with invalid entry_id.
    """
    entry_id = 123456  # invalid

    response = client.delete(f"/transmission-losses/{entry_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionLoss {entry_id} not found!"


def test_remove_transmission_loss_by_component(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all TransmissionLoss of a component.
    """
    transmission_loss = excel_file_type_create(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    component_id = transmission_loss.ref_component

    response = client.delete(f"/transmission-losses/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    deleted_entry = response.json()[0]
    assert deleted_entry["component"]["id"] == component_id


def test_remove_transmission_loss_by_component_entry_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test removing all TransmissionLoss of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.delete(f"/transmission-losses/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"TransmissionLoss for component {component_id} not found!"


def test_upload_transmission_loss(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading TransmissionLoss of a component.
    """
    dataset = dataset_create(db, normal_user_headers)
    component = source_create(db, normal_user_headers, dataset_id=dataset.id)
    component_id = component.component.id
    region = region_create(db, normal_user_headers, dataset_id=dataset.id)
    region2 = region_create(db, normal_user_headers, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name], as_matrix=True) as file:
        response = client.post(
            f"/transmission-losses/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_200_OK

        uploaded_file = response.json()
        assert uploaded_file["file"] == file.name
        assert uploaded_file["status"] == "OK"


def test_upload_transmission_loss_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading TransmissionLoss of a component, with invalid component_id.
    """
    component_id = 123456  # invalid
    with generate_excel_file(region_names=["region"], as_matrix=True) as file:
        response = client.post(
            f"/transmission-losses/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        error_detail = response.json()["detail"]
        assert error_detail == f"Component {component_id} not found!"


def test_upload_transmission_loss_bad_request(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test uploading TransmissionLoss of a component, with an unknown region in the data.
    """
    dataset = dataset_create(db, normal_user_headers)
    component = source_create(db, normal_user_headers, dataset_id=dataset.id)
    component_id = component.component.id
    region = region_create(db, normal_user_headers, dataset_id=dataset.id)
    region2 = region_create(db, normal_user_headers, dataset_id=dataset.id)

    with generate_excel_file(region_names=[region.name, region2.name, "unknown region"], as_matrix=True) as file:  # unknown region doesn't exist
        response = client.post(
            f"/transmission-losses/component/{component_id}/upload",
            headers=normal_user_headers,
            files={"file": (file.name, file.open(mode="rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_detail = response.json()["detail"]
        assert error_detail["file"] == file.name
        assert error_detail["status"] == "ERROR"


def test_download_transmission_loss(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading TransmissionLoss of a component.
    """
    transmission_loss = excel_file_type_create(TRANSMISSION_LOSS, db, normal_user_headers, transmission_component=True)
    component_id = transmission_loss.ref_component

    response = client.get(
        f"/transmission-losses/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_download_transmission_loss_component_not_found(client: TestClient, normal_user_headers: dict[str, str], db: Session):
    """
    Test downloading TransmissionLoss of a component, with invalid component_id.
    """
    component_id = 123456  # invalid

    response = client.get(
        f"/transmission-losses/component/{component_id}/download",
        headers=normal_user_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_detail = response.json()["detail"]
    assert error_detail == f"Component {component_id} not found!"
