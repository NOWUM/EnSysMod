from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils import data_generator as data_gen

from ensysmod.schemas import EnergyModelCreate


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
    existing_model.override_parameters = []
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


def test_create_energy_model_with_override_parameters(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy model with override parameters.
    """
    create_request = data_gen.random_energy_model_create(db)
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_model = response.json()
    assert created_model["name"] == create_request.name
    assert created_model["override_parameters"][0]["attribute"] == "yearly_limit"
    assert created_model["override_parameters"][0]["operation"] == "set"
    assert created_model["override_parameters"][0]["value"] == 366.6


def test_create_energy_model_with_optimization_parameters(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy model with optimization parameters.
    """
    create_request = data_gen.random_energy_model_create(db)
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_model = response.json()
    assert created_model["name"] == create_request.name
    assert created_model["optimization_parameters"][0]["start_year"] == 2020
    assert created_model["optimization_parameters"][0]["end_year"] == 2050
    assert created_model["optimization_parameters"][0]["number_of_steps"] == 3
    assert created_model["optimization_parameters"][0]["years_per_step"] == 10


# TODO Add more test cases
