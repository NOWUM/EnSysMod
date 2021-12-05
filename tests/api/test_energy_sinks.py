from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergySinkCreate, EnergySink
from tests.api.test_datasets import get_random_existing_dataset
from tests.api.test_energy_commodities import get_random_existing_energy_commodity
from tests.utils.utils import random_lower_string


def get_random_energy_sink_create(db: Session) -> EnergySinkCreate:
    dataset = get_random_existing_dataset(db)
    commodity = get_random_existing_energy_commodity(db)
    return EnergySinkCreate(
        ref_dataset=dataset.id,
        name=f"Energy Sink {random_lower_string()}",
        description="Description",
        commodity=commodity.name,
    )


def get_random_existing_energy_sink(db: Session) -> EnergySink:
    create_request = get_random_energy_sink_create(db)
    return crud.energy_sink.create(db=db, obj_in=create_request)


def test_create_energy_sink(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy sink.
    """
    create_request = get_random_energy_sink_create(db)
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_sinks = response.json()
    assert created_sinks["component"]["name"] == create_request.name
    assert created_sinks["component"]["description"] == create_request.description
    assert created_sinks["component"]["type"] == EnergyComponentType.SINK.value
    assert created_sinks["commodity"]["name"] == create_request.commodity


def test_create_existing_energy_sink(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing energy sink.
    """
    create_request = get_random_energy_sink_create(db)
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_sink_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy sink.
    """
    create_request = get_random_energy_sink_create(db)
    create_request.ref_dataset = 0  # ungültige Anfrage
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_energy_sink_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy sink.
    """
    create_request = get_random_energy_sink_create(db)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sinks/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
