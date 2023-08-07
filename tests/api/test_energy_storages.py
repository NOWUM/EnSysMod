from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils import data_generator
from tests.utils.assertions import assert_energy_component
from tests.utils.utils import clear_database


def test_get_all_energy_storages(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all energy storages.
    """
    clear_database(db)
    storage1 = data_generator.random_existing_energy_storage(db)
    storage2 = data_generator.random_existing_energy_storage(db)

    response = client.get("/storages/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    storage_list = response.json()
    assert len(storage_list) == 2
    assert storage_list[0]["component"]["name"] == storage1.component.name
    assert storage_list[0]["component"]["id"] == storage1.component.id
    assert storage_list[1]["component"]["name"] == storage2.component.name
    assert storage_list[1]["component"]["id"] == storage2.component.id


def test_create_storage(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy storage.
    """
    create_request = data_generator.random_energy_storage_create(db)
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_storage = response.json()
    assert_energy_component(created_storage["component"], create_request, EnergyComponentType.STORAGE)
    assert created_storage["commodity"]["name"] == create_request.commodity


def test_create_existing_storage(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing energy storage.
    """
    create_request = data_generator.random_energy_storage_create(db)
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_storage_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy storage.
    """
    create_request = data_generator.random_energy_storage_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_storage_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy storage.
    """
    create_request = data_generator.random_energy_storage_create(db)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
