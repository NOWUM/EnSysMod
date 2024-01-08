from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_storages import (
    storage_create,
    storage_create_request,
)


def test_get_energy_storage_by_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all energy storages of a dataset.
    """
    dataset = dataset_create(db, normal_user_headers)
    storage1 = storage_create(db, normal_user_headers, dataset_id=dataset.id)
    storage2 = storage_create(db, normal_user_headers, dataset_id=dataset.id)

    response = client.get("/storages/", headers=normal_user_headers, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    storage_list = response.json()
    assert len(storage_list) == 2
    assert storage_list[0]["component"]["name"] == storage1.component.name
    assert storage_list[0]["component"]["id"] == storage1.component.id
    assert storage_list[1]["component"]["name"] == storage2.component.name
    assert storage_list[1]["component"]["id"] == storage2.component.id


def test_create_storage(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy storage.
    """
    create_request = storage_create_request(db, normal_user_headers)
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_storage = response.json()
    assert_energy_component(created_storage["component"], create_request, EnergyComponentType.STORAGE)
    assert created_storage["commodity"]["name"] == create_request.commodity


def test_create_existing_storage(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an existing energy storage.
    """
    create_request = storage_create_request(db, normal_user_headers)
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_storage_unknown_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy storage.
    """
    create_request = storage_create_request(db, normal_user_headers)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_storage_unknown_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy storage.
    """
    create_request = storage_create_request(db, normal_user_headers)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
