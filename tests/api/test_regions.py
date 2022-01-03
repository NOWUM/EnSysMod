from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import RegionCreate
from tests.utils import data_generator as data_gen


def test_create_region(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a region.
    """
    create_request = data_gen.random_region_create(db)
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_region = response.json()
    assert created_region["name"] == create_request.name
    assert created_region["dataset"]["id"] == create_request.ref_dataset


def test_create_existing_region(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing region.
    """
    existing_region = data_gen.random_existing_region(db)
    create_request = RegionCreate(**jsonable_encoder(existing_region))
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_region_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a region.
    """
    create_request = data_gen.random_region_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
