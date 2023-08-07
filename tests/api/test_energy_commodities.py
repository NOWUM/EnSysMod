from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyCommodityCreate
from tests.utils import data_generator
from tests.utils.utils import clear_database


def test_get_all_commodities(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all commodities.
    """
    clear_database(db)
    commodity1 = data_generator.random_existing_energy_commodity(db)
    commodity2 = data_generator.random_existing_energy_commodity(db)

    response = client.get("/commodities/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    commodity_list = response.json()
    assert len(commodity_list) == 2
    assert commodity_list[0]["name"] == commodity1.name
    assert commodity_list[0]["id"] == commodity1.id
    assert commodity_list[1]["name"] == commodity2.name
    assert commodity_list[1]["id"] == commodity2.id


def test_get_all_commodities_specific_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all commodities belonging to a specific dataset.
    """
    clear_database(db)
    commodity1 = data_generator.random_existing_energy_commodity(db)
    commodity2 = data_generator.random_existing_energy_commodity(db)

    response1 = client.get("/commodities/", headers=normal_user_headers, params={"dataset_id": commodity1.dataset.id})
    assert response1.status_code == status.HTTP_200_OK

    commodity_list1 = response1.json()
    assert len(commodity_list1) == 1
    assert commodity_list1[0]["name"] == commodity1.name
    assert commodity_list1[0]["id"] == commodity1.id

    response2 = client.get("/commodities/", headers=normal_user_headers, params={"dataset_id": commodity2.dataset.id})
    assert response2.status_code == status.HTTP_200_OK

    commodity_list2 = response2.json()
    assert len(commodity_list2) == 1
    assert commodity_list2[0]["name"] == commodity2.name
    assert commodity_list2[0]["id"] == commodity2.id


def test_get_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving a commodity.
    """
    commodity = data_generator.random_existing_energy_commodity(db)
    response = client.get(f"/commodities/{commodity.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    retrieved_commodity = response.json()
    print(retrieved_commodity)
    assert retrieved_commodity["name"] == commodity.name
    assert retrieved_commodity["id"] == commodity.id


def test_create_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy commodity.
    """
    create_request = data_generator.random_energy_commodity_create(db)
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_commodity = response.json()
    assert created_commodity["name"] == create_request.name
    assert created_commodity["dataset"]["id"] == create_request.ref_dataset
    assert created_commodity["description"] == create_request.description
    assert created_commodity["unit"] == create_request.unit


def test_create_existing_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing energy commodity.
    """
    existing_commodity = data_generator.random_existing_energy_commodity(db)
    create_request = EnergyCommodityCreate(**jsonable_encoder(existing_commodity))
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_commodity_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy commodity.
    """
    create_request = data_generator.random_energy_commodity_create(db)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases: update_commodity, remove_commodity
