from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import EnergyCommodityCreate, EnergyCommodity
from tests.api.test_datasets import get_random_existing_dataset
from tests.utils.utils import random_lower_string


def get_random_energy_commodity_create(db: Session) -> EnergyCommodityCreate:
    dataset = get_random_existing_dataset(db)
    return EnergyCommodityCreate(name=f"EnergyCommodity-{dataset.id}-" + random_lower_string(),
                                 ref_dataset=dataset.id,
                                 description="EnergyCommodity description",
                                 unit="kWh")


def get_random_existing_energy_commodity(db: Session) -> EnergyCommodity:
    create_request = get_random_energy_commodity_create(db)
    return crud.energy_commodity.create(db=db, obj_in=create_request)


def test_create_energy_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy commodity.
    """
    create_request = get_random_energy_commodity_create(db)
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_commodity = response.json()
    assert created_commodity["name"] == create_request.name
    assert created_commodity["dataset"]["id"] == create_request.ref_dataset
    assert created_commodity["description"] == create_request.description
    assert created_commodity["unit"] == create_request.unit


def test_create_existing_energy_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing energy commodity.
    """
    existing_commodity = get_random_existing_energy_commodity(db)
    create_request = EnergyCommodityCreate(**jsonable_encoder(existing_commodity))
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_commodity_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy commodity.
    """
    create_request = get_random_energy_commodity_create(db)
    create_request.ref_dataset = 0  # ungültige Anfrage
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
