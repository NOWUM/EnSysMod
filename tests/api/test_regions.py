from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import RegionCreate, RegionUpdate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.regions import new_region, region_create_request
from tests.utils.utils import random_string


def test_get_region(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a region.
    """
    region = new_region(db, user_header)
    response = client.get(f"/regions/{region.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_region = response.json()
    assert retrieved_region["name"] == region.name
    assert retrieved_region["id"] == region.id


def test_get_region_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all regions of a dataset.
    """
    dataset = new_dataset(db, user_header)
    region1 = new_region(db, user_header, dataset_id=dataset.id)
    region2 = new_region(db, user_header, dataset_id=dataset.id)

    response = client.get("/regions/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    region_list = response.json()
    assert len(region_list) == 2
    assert region_list[0]["name"] == region1.name
    assert region_list[0]["id"] == region1.id
    assert region_list[1]["name"] == region2.name
    assert region_list[1]["id"] == region2.id


def test_create_region(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a region.
    """
    create_request = region_create_request(db, user_header)
    response = client.post("/regions/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_region = response.json()
    assert created_region["name"] == create_request.name
    assert created_region["dataset"]["id"] == create_request.ref_dataset


def test_create_existing_region(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing region.
    """
    existing_region = new_region(db, user_header)
    create_request = RegionCreate(**jsonable_encoder(existing_region))
    response = client.post("/regions/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_region_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a region.
    """
    create_request = region_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/regions/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_multiple_regions_same_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating multiple regions on the same dataset.
    """
    existing_region = new_region(db, user_header)
    dataset_id = existing_region.dataset.id

    # Create a new region on the same dataset
    create_request = region_create_request(db, user_header)
    create_request.ref_dataset = dataset_id

    response = client.post("/regions/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    second_region = response.json()

    # Check that the dataset has two regions
    get_response = client.get("/regions/", headers=user_header, params={"dataset_id": dataset_id})
    assert get_response.status_code == status.HTTP_200_OK

    region_list = get_response.json()
    assert len(region_list) == 2
    assert region_list[0]["name"] == existing_region.name
    assert region_list[0]["id"] == existing_region.id
    assert region_list[1]["name"] == second_region["name"]
    assert region_list[1]["id"] == second_region["id"]


def test_update_region(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test updating a region.
    """
    existing_region = new_region(db, user_header)

    update_request = RegionUpdate(**jsonable_encoder(existing_region))
    update_request.name = f"New Region Name-{random_string()}"

    response = client.put(f"/regions/{existing_region.id}", headers=user_header, content=update_request.json())
    assert response.status_code == status.HTTP_200_OK

    updated_region = response.json()
    assert updated_region["name"] == update_request.name


def test_remove_region(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting a region.
    """
    # Create two regions in the same dataset
    region1 = new_region(db, user_header)
    dataset_id = region1.dataset.id
    region2 = new_region(db, user_header, dataset_id=dataset_id)

    # Delete the first region
    response = client.delete(f"/regions/{region1.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    # Check that the dataset only has the second region
    get_response = client.get("/regions/", headers=user_header, params={"dataset_id": dataset_id})
    assert get_response.status_code == status.HTTP_200_OK

    region_list = get_response.json()
    assert len(region_list) == 1
    assert region_list[0]["name"] == region2.name
    assert region_list[0]["id"] == region2.id
