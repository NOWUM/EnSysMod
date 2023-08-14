from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils import data_generator
from tests.utils.assertions import assert_energy_component
from tests.utils.utils import clear_database


def test_get_all_energy_sources(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all energy sources.
    """
    clear_database(db)
    source1 = data_generator.random_existing_energy_source(db)
    source2 = data_generator.random_existing_energy_source(db)

    response = client.get("/sources/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    source_list = response.json()
    assert len(source_list) == 2
    assert source_list[0]["component"]["name"] == source1.component.name
    assert source_list[0]["component"]["id"] == source1.component.id
    assert source_list[1]["component"]["name"] == source2.component.name
    assert source_list[1]["component"]["id"] == source2.component.id


def test_create_source(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy source.
    """
    create_request = data_generator.random_energy_source_create(db)
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_source = response.json()
    assert_energy_component(created_source["component"], create_request, EnergyComponentType.SOURCE)
    assert created_source["commodity"]["name"] == create_request.commodity


def test_create_existing_source(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing energy source.
    """
    create_request = data_generator.random_energy_source_create(db)
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_source_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy source.
    """
    create_request = data_generator.random_energy_source_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_source_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy source.
    """
    create_request = data_generator.random_energy_source_create(db)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
