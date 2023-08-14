from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils import data_generator
from tests.utils.assertions import assert_energy_component
from tests.utils.utils import clear_database


def test_get_all_energy_transmissions(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all energy transmissions.
    """
    clear_database(db)
    transmission1 = data_generator.random_existing_energy_transmission(db)
    transmission2 = data_generator.random_existing_energy_transmission(db)

    response = client.get("/transmissions/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    transmission_list = response.json()
    assert len(transmission_list) == 2
    assert transmission_list[0]["component"]["name"] == transmission1.component.name
    assert transmission_list[0]["component"]["id"] == transmission1.component.id
    assert transmission_list[1]["component"]["name"] == transmission2.component.name
    assert transmission_list[1]["component"]["id"] == transmission2.component.id


def test_create_transmission(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy transmission.
    """
    create_request = data_generator.random_energy_transmission_create(db)
    response = client.post("/transmissions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_transmission = response.json()
    assert_energy_component(created_transmission["component"], create_request, EnergyComponentType.TRANSMISSION)
    assert created_transmission["commodity"]["name"] == create_request.commodity


def test_create_existing_transmission(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing energy transmission.
    """
    create_request = data_generator.random_energy_transmission_create(db)
    response = client.post("/transmissions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/transmissions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_transmission_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy transmission.
    """
    create_request = data_generator.random_energy_transmission_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/transmissions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_transmission_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy transmission.
    """
    create_request = data_generator.random_energy_transmission_create(db)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/transmissions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
