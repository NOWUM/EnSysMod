from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import RegionCreate, Region
from tests.api.test_datasets import get_random_existing_dataset
from tests.utils.utils import random_lower_string


def get_random_region_create(db: Session) -> RegionCreate:
    dataset = get_random_existing_dataset(db)
    return RegionCreate(name=f"Region-{dataset.id}-" + random_lower_string(),
                        ref_dataset=dataset.id)


def get_random_existing_region(db: Session) -> Region:
    create_request = get_random_region_create(db)
    return crud.region.create(db=db, obj_in=create_request)


def test_create_region(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a region.
    """
    create_request = get_random_region_create(db)
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_region = response.json()
    assert created_region["name"] == create_request.name
    assert created_region["dataset"]["id"] == create_request.ref_dataset


def test_create_existing_region(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing region.
    """
    existing_region = get_random_existing_region(db)
    create_request = RegionCreate(**jsonable_encoder(existing_region))
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_region_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a region.
    """
    create_request = get_random_region_create(db)
    create_request.ref_dataset = 0  # ungültige Anfrage
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
