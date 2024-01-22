from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_sources import new_source, source_create_request


def test_get_energy_source_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all energy sources of a dataset.
    """
    dataset = new_dataset(db, user_header)
    source1 = new_source(db, user_header, dataset_id=dataset.id)
    source2 = new_source(db, user_header, dataset_id=dataset.id)

    response = client.get("/sources/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    source_list = response.json()
    assert len(source_list) == 2
    assert source_list[0]["component"]["name"] == source1.component.name
    assert source_list[0]["component"]["id"] == source1.component.id
    assert source_list[1]["component"]["name"] == source2.component.name
    assert source_list[1]["component"]["id"] == source2.component.id


def test_create_source(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy source.
    """
    create_request = source_create_request(db, user_header)
    response = client.post("/sources/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK

    created_source = response.json()
    assert_energy_component(created_source["component"], create_request, EnergyComponentType.SOURCE)
    assert created_source["commodity"]["name"] == create_request.commodity


def test_create_existing_source(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy source.
    """
    create_request = source_create_request(db, user_header)
    response = client.post("/sources/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sources/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_source_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy source.
    """
    create_request = source_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/sources/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_source_unknown_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy source.
    """
    create_request = source_create_request(db, user_header)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sources/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
