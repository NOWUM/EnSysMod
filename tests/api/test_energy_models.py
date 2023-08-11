from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyModelCreate, EnergyModelUpdate
from tests.utils import data_generator
from tests.utils.utils import clear_database, random_lower_string


def test_get_all_models(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all energy models.
    """
    clear_database(db)
    model1 = data_generator.random_existing_energy_model(db)
    model2 = data_generator.random_existing_energy_model(db)

    response = client.get("/models/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    model_list = response.json()
    assert len(model_list) == 2
    assert model_list[0]["name"] == model1.name
    assert model_list[0]["dataset"]["id"] == model1.dataset.id
    assert model_list[1]["name"] == model2.name
    assert model_list[1]["dataset"]["id"] == model2.dataset.id


def test_get_model(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving an energy model.
    """
    model = data_generator.random_existing_energy_model(db)
    response = client.get(f"/models/{model.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    retrieved_model = response.json()
    assert retrieved_model["name"] == model.name
    assert retrieved_model["dataset"]["id"] == model.dataset.id


def test_create_model(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy model.
    """
    create_request = data_generator.random_energy_model_create(db)
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_model = response.json()
    assert created_model["name"] == create_request.name
    assert created_model["dataset"]["id"] == create_request.ref_dataset
    assert created_model["description"] == create_request.description


def test_create_existing_model(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing energy model.
    """
    existing_model = data_generator.random_existing_energy_model(db)
    existing_model.override_parameters = []
    create_request = EnergyModelCreate(**jsonable_encoder(existing_model))
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_model_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy model.
    """
    create_request = data_generator.random_energy_model_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_energy_model_with_override_parameters(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy model with override parameters.
    """
    create_request = data_generator.random_energy_model_create(db)
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_model = response.json()
    assert created_model["name"] == create_request.name
    assert created_model["override_parameters"][0]["attribute"] == "yearly_limit"
    assert created_model["override_parameters"][0]["operation"] == "set"
    assert created_model["override_parameters"][0]["value"] == 366.6


def test_create_energy_model_with_optimization_parameters(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy model with optimization parameters.
    """
    create_request = data_generator.random_energy_model_create(db)
    response = client.post("/models/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_model = response.json()
    assert created_model["name"] == create_request.name
    assert created_model["optimization_parameters"][0]["start_year"] == 2020
    assert created_model["optimization_parameters"][0]["end_year"] == 2050
    assert created_model["optimization_parameters"][0]["number_of_steps"] == 3
    assert created_model["optimization_parameters"][0]["years_per_step"] == 10


def test_update_energy_model(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test updating an energy model.
    """
    existing_model = data_generator.random_existing_energy_model(db)
    print(existing_model.name)

    update_request = EnergyModelUpdate(**jsonable_encoder(existing_model))
    update_request.name = f"New Energy Model Name-{random_lower_string()}"

    print(update_request.json())

    response = client.put(
        f"/models/{existing_model.id}",
        headers=normal_user_headers,
        data=update_request.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    updated_model = response.json()
    assert updated_model["name"] == update_request.name


def test_remove_energy_model(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test deleting an energy_model.
    """
    existing_model = data_generator.random_existing_energy_model(db)
    response = client.delete(
        f"/models/{existing_model.id}",
        headers=normal_user_headers
    )
    assert response.status_code == status.HTTP_200_OK
