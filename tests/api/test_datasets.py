from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import DatasetUpdate
from tests.utils.data_generator.datasets import dataset_create_request, new_dataset
from tests.utils.utils import assert_response, clear_database, random_string


def test_get_all_datasets(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving all datasets.
    """
    clear_database(db)
    dataset1 = new_dataset(db, user_header)
    dataset2 = new_dataset(db, user_header)

    response = client.get("/datasets/", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert_response(response.json()[0], dataset1)
    assert_response(response.json()[1], dataset2)


def test_get_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a dataset.
    """
    dataset = new_dataset(db, user_header)
    response = client.get(f"/datasets/{dataset.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), dataset)


def test_create_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a dataset.
    """
    create_request = dataset_create_request(db, user_header)

    response = client.post("/datasets/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


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
    existing_dataset = new_dataset(db, user_header, hours_per_time_step=2)

    update_request = DatasetUpdate(
        name=f"New Dataset Name-{random_string()}",
        description=f"New Dataset Description-{random_string()}",
    )

    response = client.put(f"/datasets/{existing_dataset.id}", headers=user_header, content=update_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), update_request)


def test_remove_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting a dataset.
    """
    existing_dataset = new_dataset(db, user_header)
    response = client.delete(f"/datasets/{existing_dataset.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
