from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils import data_generator as data_gen
from tests.utils.assertions import assert_energy_component


def test_create_energy_storage(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy storage.
    """
    create_request = data_gen.random_energy_storage_create(db)
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_storage = response.json()
    assert_energy_component(created_storage["component"], create_request, EnergyComponentType.STORAGE)
    assert created_storage["commodity"]["name"] == create_request.commodity


def test_create_existing_energy_storage(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing energy storage.
    """
    create_request = data_gen.random_energy_storage_create(db)
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_storage_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy storage.
    """
    create_request = data_gen.random_energy_storage_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_energy_storage_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy storage.
    """
    create_request = data_gen.random_energy_storage_create(db)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/storages/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
