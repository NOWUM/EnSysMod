from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.energy_sources import (
    source_create,
    source_create_request,
)
from tests.utils.utils import clear_database


def test_get_all_energy_sources(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all energy sources.
    """
    clear_database(db)
    source1 = source_create(db, normal_user_headers)
    source2 = source_create(db, normal_user_headers)

    response = client.get("/sources/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    source_list = response.json()
    assert len(source_list) == 2
    assert source_list[0]["component"]["name"] == source1.component.name
    assert source_list[0]["component"]["id"] == source1.component.id
    assert source_list[1]["component"]["name"] == source2.component.name
    assert source_list[1]["component"]["id"] == source2.component.id


def test_create_source(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy source.
    """
    create_request = source_create_request(db, normal_user_headers)
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_source = response.json()
    assert_energy_component(created_source["component"], create_request, EnergyComponentType.SOURCE)
    assert created_source["commodity"]["name"] == create_request.commodity


def test_create_existing_source(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an existing energy source.
    """
    create_request = source_create_request(db, normal_user_headers)
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_source_unknown_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy source.
    """
    create_request = source_create_request(db, normal_user_headers)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_source_unknown_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy source.
    """
    create_request = source_create_request(db, normal_user_headers)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
