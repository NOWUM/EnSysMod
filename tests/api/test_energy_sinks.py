from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils import data_generator
from tests.utils.assertions import assert_energy_component
from tests.utils.utils import clear_database


def test_get_all_energy_sinks(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all energy sinks.
    """
    clear_database(db)
    sink1 = data_generator.random_existing_energy_sink(db)
    sink2 = data_generator.random_existing_energy_sink(db)

    response = client.get("/sinks/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    sink_list = response.json()
    assert len(sink_list) == 2
    assert sink_list[0]["component"]["name"] == sink1.component.name
    assert sink_list[0]["component"]["id"] == sink1.component.id
    assert sink_list[1]["component"]["name"] == sink2.component.name
    assert sink_list[1]["component"]["id"] == sink2.component.id


def test_create_sink(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy sink.
    """
    create_request = data_generator.random_energy_sink_create(db)
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_sinks = response.json()
    assert_energy_component(created_sinks["component"], create_request, EnergyComponentType.SINK)
    assert created_sinks["commodity"]["name"] == create_request.commodity


def test_create_existing_sink(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing energy sink.
    """
    create_request = data_generator.random_energy_sink_create(db)
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_sink_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy sink.
    """
    create_request = data_generator.random_energy_sink_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_sink_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy sink.
    """
    create_request = data_generator.random_energy_sink_create(db)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
