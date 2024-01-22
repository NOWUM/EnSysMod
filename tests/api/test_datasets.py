from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import DatasetUpdate
from tests.utils.data_generator.datasets import dataset_create_request, new_dataset
from tests.utils.utils import clear_database, random_string


def test_get_all_datasets(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving all datasets.
    """
    clear_database(db)
    dataset1 = new_dataset(db, user_header)
    dataset2 = new_dataset(db, user_header)

    response = client.get("/datasets/", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    dataset_list = response.json()
    assert len(dataset_list) == 2
    assert dataset_list[0]["name"] == dataset1.name
    assert dataset_list[0]["id"] == dataset1.id
    assert dataset_list[1]["name"] == dataset2.name
    assert dataset_list[1]["id"] == dataset2.id


def test_get_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a dataset.
    """
    dataset = new_dataset(db, user_header)
    response = client.get(f"/datasets/{dataset.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_dataset = response.json()
    assert retrieved_dataset["name"] == dataset.name
    assert retrieved_dataset["id"] == dataset.id


def test_create_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a dataset.
    """
    create_request = dataset_create_request(db, user_header)

    response = client.post("/datasets/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK

    created_dataset = response.json()
    assert created_dataset["name"] == create_request.name
    assert created_dataset["description"] == create_request.description


def test_create_existing_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing dataset.
    """
    create_request = dataset_create_request(db, user_header)
    response = client.post("/datasets/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/datasets/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test updating a dataset.
    """
    existing_dataset = new_dataset(db, user_header)

    update_request = DatasetUpdate(**jsonable_encoder(existing_dataset))
    update_request.name = f"New Dataset Name-{random_string()}"
    update_request.description = f"New Dataset Description-{random_string()}"

    response = client.put(f"/datasets/{existing_dataset.id}", headers=user_header, content=update_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK

    updated_dataset = response.json()
    assert updated_dataset["name"] == update_request.name
    assert updated_dataset["description"] == update_request.description


def test_remove_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting a dataset.
    """
    existing_dataset = new_dataset(db, user_header)
    response = client.delete(f"/datasets/{existing_dataset.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
