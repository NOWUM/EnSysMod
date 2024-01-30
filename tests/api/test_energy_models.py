from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyModelUpdate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_models import energy_model_create_request, new_energy_model
from tests.utils.utils import assert_response, random_string


def test_get_model(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving an energy model.
    """
    model = new_energy_model(db, user_header)
    response = client.get(f"/models/{model.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), model)


def test_get_model_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all models of a dataset.
    """
    dataset = new_dataset(db, user_header)
    model1 = new_energy_model(db, user_header, dataset_id=dataset.id)
    model2 = new_energy_model(db, user_header, dataset_id=dataset.id)

    response = client.get("/models/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert_response(response.json()[0], model1)
    assert_response(response.json()[1], model2)


def test_create_model(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy model.
    """
    create_request = energy_model_create_request(db, user_header)
    response = client.post("/models/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_existing_model(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy model.
    """
    create_request = energy_model_create_request(db, user_header)
    response = client.post("/models/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/models/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_model_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy model.
    """
    create_request = energy_model_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/models/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_energy_model_with_override_parameters(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy model with override parameters.
    """
    create_request = energy_model_create_request(db, user_header, generate_override_parameters=True)
    response = client.post("/models/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_energy_model_with_optimization_parameters(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy model with optimization parameters.
    """
    create_request = energy_model_create_request(db, user_header, generate_optimization_parameters=True)
    response = client.post("/models/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_update_energy_model(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test updating an energy model.
    """
    existing_model = new_energy_model(db, user_header)

    update_request = EnergyModelUpdate(name=f"New Energy Model Name-{random_string()}")

    response = client.put(f"/models/{existing_model.id}", headers=user_header, content=update_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), update_request)


def test_remove_energy_model(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting an energy_model.
    """
    existing_model = new_energy_model(db, user_header)
    response = client.delete(f"/models/{existing_model.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), existing_model)
