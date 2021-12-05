from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergySourceCreate, EnergySource
from tests.api.test_datasets import get_random_existing_dataset
from tests.api.test_energy_commodities import get_random_existing_energy_commodity
from tests.utils.utils import random_lower_string


def get_random_energy_source_create(db: Session) -> EnergySourceCreate:
    dataset = get_random_existing_dataset(db)
    commodity = get_random_existing_energy_commodity(db)
    return EnergySourceCreate(
        ref_dataset=dataset.id,
        name=f"Energy Source {random_lower_string()}",
        description="Description",
        commodity=commodity.name,
    )


def get_random_existing_energy_source(db: Session) -> EnergySource:
    create_request = get_random_energy_source_create(db)
    return crud.energy_source.create(db=db, obj_in=create_request)


def test_create_energy_source(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy source.
    """
    create_request = get_random_energy_source_create(db)
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_source = response.json()
    assert created_source["component"]["name"] == create_request.name
    assert created_source["component"]["description"] == create_request.description
    assert created_source["component"]["type"] == EnergyComponentType.SOURCE.value
    assert created_source["commodity"]["name"] == create_request.commodity


def test_create_existing_energy_source(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing energy source.
    """
    create_request = get_random_energy_source_create(db)
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_source_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy source.
    """
    create_request = get_random_energy_source_create(db)
    create_request.ref_dataset = 0  # ungültige Anfrage
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_energy_source_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy source.
    """
    create_request = get_random_energy_source_create(db)
    create_request.commodity = "0"  # ungültige Anfrage
    response = client.post("/sources/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
