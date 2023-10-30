from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.energy_sinks import sink_create, sink_create_request
from tests.utils.utils import clear_database


def test_get_all_energy_sinks(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all energy sinks.
    """
    clear_database(db)
    sink1 = sink_create(db, normal_user_headers)
    sink2 = sink_create(db, normal_user_headers)

    response = client.get("/sinks/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    sink_list = response.json()
    assert len(sink_list) == 2
    assert sink_list[0]["component"]["name"] == sink1.component.name
    assert sink_list[0]["component"]["id"] == sink1.component.id
    assert sink_list[1]["component"]["name"] == sink2.component.name
    assert sink_list[1]["component"]["id"] == sink2.component.id


def test_create_sink(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, normal_user_headers)
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_sinks = response.json()
    assert_energy_component(created_sinks["component"], create_request, EnergyComponentType.SINK)
    assert created_sinks["commodity"]["name"] == create_request.commodity


def test_create_existing_sink(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an existing energy sink.
    """
    create_request = sink_create_request(db, normal_user_headers)
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_sink_unknown_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, normal_user_headers)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_sink_unknown_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, normal_user_headers)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
