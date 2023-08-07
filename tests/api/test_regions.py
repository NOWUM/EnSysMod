from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import RegionCreate
from tests.utils import data_generator
from tests.utils.utils import clear_database


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

# TODO Add more test cases: update_region, remove_region
