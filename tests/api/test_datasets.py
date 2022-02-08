from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import DatasetCreate, DatasetUpdate
from tests.utils import data_generator as data_gen
from tests.utils.utils import random_lower_string


def test_create_dataset(client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test creating a dataset.
    """
    # Create a dataset
    create_request = data_gen.random_dataset_create()

    response = client.post(
        "/datasets/",
        headers=normal_user_headers,
        data=create_request.json()
    )
    assert response.status_code == status.HTTP_200_OK

    created_dataset = response.json()
    assert created_dataset['name'] == create_request.name
    assert created_dataset['description'] == create_request.description


def test_create_existing_dataset(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test creating an existing dataset.
    """
    existing_dataset = data_gen.random_existing_dataset(db)
    print(existing_dataset.name)
    create_request = DatasetCreate(**jsonable_encoder(existing_dataset))
    response = client.post(
        "/datasets/",
        headers=normal_user_headers,
        data=create_request.json()
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_existing_dataset(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test updating an existing dataset.
    """
    existing_dataset = data_gen.random_existing_dataset(db)
    print(existing_dataset.name)
    update_request = DatasetUpdate(**jsonable_encoder(existing_dataset))
    new_description = random_lower_string()
    update_request.description = new_description
    response = client.put(
        f"/datasets/{existing_dataset.id}",
        headers=normal_user_headers,
        data=update_request.json()
    )
    assert response.status_code == status.HTTP_200_OK

    updated_dataset = response.json()
    assert updated_dataset['name'] == update_request.name
    assert updated_dataset['description'] == update_request.description


def test_delete_existing_dataset(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test deleting an existing dataset.
    """
    existing_dataset = data_gen.random_existing_dataset(db)
    response = client.delete(
        f"/datasets/{existing_dataset.id}",
        headers=normal_user_headers
    )
    assert response.status_code == status.HTTP_200_OK
