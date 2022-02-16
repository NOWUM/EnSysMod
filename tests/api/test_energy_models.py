from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyModelCreate
from tests.utils import data_generator as data_gen


def test_create_energy_model(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy model.
    """
    create_request = data_gen.random_energy_model_create(db)
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_model = response.json()
    assert created_model["name"] == create_request.name
    assert created_model["dataset"]["id"] == create_request.ref_dataset
    assert created_model["description"] == create_request.description


def test_create_existing_energy_model(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing energy model.
    """
    existing_model = data_gen.random_existing_energy_model(db)
    existing_model.parameters = []
    create_request = EnergyModelCreate(**jsonable_encoder(existing_model))
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_model_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy model.
    """
    create_request = data_gen.random_energy_model_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
