from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import RegionCreate, RegionUpdate
from tests.utils import data_generator
from tests.utils.utils import clear_database, random_lower_string


def test_get_all_regions(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all regions.
    """
    clear_database(db)
    region1 = data_generator.random_existing_region(db)
    region2 = data_generator.random_existing_region(db)

    response = client.get("/regions/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    region_list = response.json()
    assert len(region_list) == 2
    assert region_list[0]["name"] == region1.name
    assert region_list[0]["id"] == region1.id
    assert region_list[1]["name"] == region2.name
    assert region_list[1]["id"] == region2.id


def test_get_all_regions_specific_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all regions belonging to a specific dataset.
    """
    clear_database(db)
    region1 = data_generator.random_existing_region(db)
    region2 = data_generator.random_existing_region(db)

    response1 = client.get("/regions/", headers=normal_user_headers, params={"dataset_id": region1.dataset.id})
    assert response1.status_code == status.HTTP_200_OK

    region_list1 = response1.json()
    assert len(region_list1) == 1
    assert region_list1[0]["name"] == region1.name
    assert region_list1[0]["id"] == region1.id

    response2 = client.get("/regions/", headers=normal_user_headers, params={"dataset_id": region2.dataset.id})
    assert response2.status_code == status.HTTP_200_OK

    region_list2 = response2.json()
    assert len(region_list2) == 1
    assert region_list2[0]["name"] == region2.name
    assert region_list2[0]["id"] == region2.id


def test_get_region(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving a region.
    """
    region = data_generator.random_existing_region(db)
    response = client.get(f"/regions/{region.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    retrieved_region = response.json()
    print(retrieved_region)
    assert retrieved_region["name"] == region.name
    assert retrieved_region["id"] == region.id


def test_create_region(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a region.
    """
    create_request = data_generator.random_region_create(db)
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_region = response.json()
    assert created_region["name"] == create_request.name
    assert created_region["dataset"]["id"] == create_request.ref_dataset


def test_create_existing_region(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing region.
    """
    existing_region = data_generator.random_existing_region(db)
    create_request = RegionCreate(**jsonable_encoder(existing_region))
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_region_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a region.
    """
    create_request = data_generator.random_region_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_multiple_regions_same_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating multiple regions on the same dataset.
    """
    existing_region = data_generator.random_existing_region(db)
    dataset_id = existing_region.dataset.id

    # Create a new region on the same dataset
    create_request = data_generator.random_region_create(db)
    create_request.ref_dataset = dataset_id

    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    second_region = response.json()

    # Check that the dataset has two regions
    get_response = client.get(
        "/regions/",
        headers=normal_user_headers,
        params={"dataset_id": dataset_id},
    )
    assert get_response.status_code == status.HTTP_200_OK

    region_list = get_response.json()
    assert len(region_list) == 2
    assert region_list[0]["name"] == existing_region.name
    assert region_list[0]["id"] == existing_region.id
    assert region_list[1]["name"] == second_region["name"]
    assert region_list[1]["id"] == second_region["id"]


def test_update_region(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test updating a region.
    """
    existing_region = data_generator.random_existing_region(db)
    print(existing_region.name)

    update_request = RegionUpdate(**jsonable_encoder(existing_region))
    update_request.name = f"New Region Name-{random_lower_string()}"

    response = client.put(
        f"/regions/{existing_region.id}",
        headers=normal_user_headers,
        data=update_request.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    updated_region = response.json()
    assert updated_region["name"] == update_request.name


def test_remove_region(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test deleting a region.
    """
    # Create a dataset with two commodities
    first_region = data_generator.random_existing_region(db)
    dataset_id = first_region.dataset.id

    create_request = data_generator.random_region_create(db)
    create_request.ref_dataset = dataset_id

    response = client.post("/regions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    second_region = response.json()

    # Delete the first region
    response = client.delete(f"/regions/{first_region.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    # Check that the dataset only has the second region
    get_response = client.get(
        "/regions/",
        headers=normal_user_headers,
        params={"dataset_id": dataset_id},
    )
    assert get_response.status_code == status.HTTP_200_OK

    region_list = get_response.json()
    assert len(region_list) == 1
    assert region_list[0]["name"] == second_region["name"]
    assert region_list[0]["id"] == second_region["id"]
