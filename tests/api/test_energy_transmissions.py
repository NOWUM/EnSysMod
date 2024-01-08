from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_transmissions import (
    transmission_create,
    transmission_create_request,
)


def test_get_energy_transmission_by_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test getting all energy transmissions of a dataset.
    """
    dataset = dataset_create(db, normal_user_headers)
    transmission1 = transmission_create(db, normal_user_headers, dataset_id=dataset.id)
    transmission2 = transmission_create(db, normal_user_headers, dataset_id=dataset.id)

    response = client.get("/transmissions/", headers=normal_user_headers, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    transmission_list = response.json()
    assert len(transmission_list) == 2
    assert transmission_list[0]["component"]["name"] == transmission1.component.name
    assert transmission_list[0]["component"]["id"] == transmission1.component.id
    assert transmission_list[1]["component"]["name"] == transmission2.component.name
    assert transmission_list[1]["component"]["id"] == transmission2.component.id


def test_create_transmission(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy transmission.
    """
    create_request = transmission_create_request(db, normal_user_headers)
    response = client.post("/transmissions/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_transmission = response.json()
    assert_energy_component(created_transmission["component"], create_request, EnergyComponentType.TRANSMISSION)
    assert created_transmission["commodity"]["name"] == create_request.commodity


def test_create_existing_transmission(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an existing energy transmission.
    """
    create_request = transmission_create_request(db, normal_user_headers)
    response = client.post("/transmissions/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/transmissions/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_transmission_unknown_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy transmission.
    """
    create_request = transmission_create_request(db, normal_user_headers)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/transmissions/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_transmission_unknown_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy transmission.
    """
    create_request = transmission_create_request(db, normal_user_headers)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/transmissions/", headers=normal_user_headers, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
