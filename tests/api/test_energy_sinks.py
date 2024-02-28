from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_sinks import new_sink, sink_create_request
from tests.utils.utils import assert_response


def test_get_energy_sink_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all energy sinks of a dataset.
    """
    dataset = new_dataset(db, user_header)
    sink1 = new_sink(db, user_header, dataset_id=dataset.id)
    sink2 = new_sink(db, user_header, dataset_id=dataset.id)

    response = client.get("/sinks/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert_response(response.json()[0], sink1)
    assert_response(response.json()[1], sink2)


def test_create_sink(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, user_header)
    response = client.post("/sinks/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_existing_sink(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy sink.
    """
    create_request = sink_create_request(db, user_header)
    response = client.post("/sinks/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sinks/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_sink_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/sinks/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_sink_unknown_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy sink.
    """
    create_request = sink_create_request(db, user_header)
    create_request.commodity_name = "0"  # ungültige Anfrage
    response = client.post("/sinks/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
