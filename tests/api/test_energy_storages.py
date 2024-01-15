from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_storages import new_storage, storage_create_request


def test_get_energy_storage_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all energy storages of a dataset.
    """
    dataset = new_dataset(db, user_header)
    storage1 = new_storage(db, user_header, dataset_id=dataset.id)
    storage2 = new_storage(db, user_header, dataset_id=dataset.id)

    response = client.get("/storages/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    storage_list = response.json()
    assert len(storage_list) == 2
    assert storage_list[0]["component"]["name"] == storage1.component.name
    assert storage_list[0]["component"]["id"] == storage1.component.id
    assert storage_list[1]["component"]["name"] == storage2.component.name
    assert storage_list[1]["component"]["id"] == storage2.component.id


def test_create_storage(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy storage.
    """
    create_request = storage_create_request(db, user_header)
    response = client.post("/storages/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_storage = response.json()
    assert_energy_component(created_storage["component"], create_request, EnergyComponentType.STORAGE)
    assert created_storage["commodity"]["name"] == create_request.commodity


def test_create_existing_storage(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy storage.
    """
    create_request = storage_create_request(db, user_header)
    response = client.post("/storages/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/storages/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_storage_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy storage.
    """
    create_request = storage_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/storages/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_storage_unknown_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy storage.
    """
    create_request = storage_create_request(db, user_header)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/storages/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
