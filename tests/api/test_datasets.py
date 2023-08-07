from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import DatasetCreate, DatasetUpdate
from tests.utils import data_generator
from tests.utils.utils import clear_database, random_lower_string


def test_get_all_datasets(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all datasets.
    """
    clear_database(db)
    dataset1 = data_generator.random_existing_dataset(db)
    dataset2 = data_generator.random_existing_dataset(db)

    response = client.get("/datasets/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    dataset_list = response.json()
    assert len(dataset_list) == 2
    assert dataset_list[0]["name"] == dataset1.name
    assert dataset_list[0]["id"] == dataset1.id
    assert dataset_list[1]["name"] == dataset2.name
    assert dataset_list[1]["id"] == dataset2.id


def test_get_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving a dataset.
    """
    dataset = data_generator.random_existing_dataset(db)
    response = client.get(f"/datasets/{dataset.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    retrieved_dataset = response.json()
    assert retrieved_dataset["name"] == dataset.name
    assert retrieved_dataset["id"] == dataset.id


def test_create_dataset(client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test creating a dataset.
    """
    # Create a dataset
    create_request = data_generator.random_dataset_create()

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
    existing_dataset = data_generator.random_existing_dataset(db)
    print(existing_dataset.name)
    create_request = DatasetCreate(**jsonable_encoder(existing_dataset))
    response = client.post(
        "/datasets/",
        headers=normal_user_headers,
        data=create_request.json()
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_dataset(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test updating a dataset.
    """
    existing_dataset = data_generator.random_existing_dataset(db)
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


def test_remove_dataset(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test deleting a dataset.
    """
    existing_dataset = data_generator.random_existing_dataset(db)
    response = client.delete(
        f"/datasets/{existing_dataset.id}",
        headers=normal_user_headers
    )
    assert response.status_code == status.HTTP_200_OK
