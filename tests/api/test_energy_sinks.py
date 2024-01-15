from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_sinks import new_sink, sink_create_request


def test_get_energy_sink_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all energy sinks of a dataset.
    """
    dataset = new_dataset(db, user_header)
    sink1 = new_sink(db, user_header, dataset_id=dataset.id)
    sink2 = new_sink(db, user_header, dataset_id=dataset.id)

    response = client.get("/sinks/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    sink_list = response.json()
    assert len(sink_list) == 2
    assert sink_list[0]["component"]["name"] == sink1.component.name
    assert sink_list[0]["component"]["id"] == sink1.component.id
    assert sink_list[1]["component"]["name"] == sink2.component.name
    assert sink_list[1]["component"]["id"] == sink2.component.id


def test_create_sink(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, user_header)
    response = client.post("/sinks/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_sinks = response.json()
    assert_energy_component(created_sinks["component"], create_request, EnergyComponentType.SINK)
    assert created_sinks["commodity"]["name"] == create_request.commodity


def test_create_existing_sink(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy sink.
    """
    create_request = sink_create_request(db, user_header)
    response = client.post("/sinks/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sinks/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_sink_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/sinks/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_sink_unknown_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, user_header)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sinks/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
