from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyCommodityCreate, EnergyCommodityUpdate
from tests.utils import data_generator
from tests.utils.utils import clear_database, random_lower_string


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


def test_create_multiple_commodities_same_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating multiple commodities on the same dataset.
    """
    existing_commodity = data_generator.random_existing_energy_commodity(db)
    dataset_id = existing_commodity.dataset.id

    # Create a new commodity on the same dataset
    create_request = data_generator.random_energy_commodity_create(db)
    create_request.ref_dataset = dataset_id

    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    second_commodity = response.json()

    # Check that the dataset has two commodities
    get_response = client.get(
        "/commodities/",
        headers=normal_user_headers,
        params={"dataset_id": dataset_id},
    )
    assert get_response.status_code == status.HTTP_200_OK

    commodity_list = get_response.json()
    assert len(commodity_list) == 2
    assert commodity_list[0]["name"] == existing_commodity.name
    assert commodity_list[0]["id"] == existing_commodity.id
    assert commodity_list[1]["name"] == second_commodity["name"]
    assert commodity_list[1]["id"] == second_commodity["id"]


def test_update_commodity(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test updating a commodity.
    """
    existing_commodity = data_generator.random_existing_energy_commodity(db)
    print(existing_commodity.name)

    update_request = EnergyCommodityUpdate(**jsonable_encoder(existing_commodity))
    update_request.name = f"New Commodity Name-{random_lower_string()}"
    update_request.unit = f"New Commodity Unit-{random_lower_string()}"
    update_request.description = f"New Commodity Description-{random_lower_string()}"

    response = client.put(
        f"/commodities/{existing_commodity.id}",
        headers=normal_user_headers,
        data=update_request.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    updated_commodity = response.json()
    assert updated_commodity["name"] == update_request.name
    assert updated_commodity["unit"] == update_request.unit
    assert updated_commodity["description"] == update_request.description


def test_remove_commodity(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test deleting a commodity.
    """
    # Create a dataset with two commodities
    first_commodity = data_generator.random_existing_energy_commodity(db)
    dataset_id = first_commodity.dataset.id

    create_request = data_generator.random_energy_commodity_create(db)
    create_request.ref_dataset = dataset_id

    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    second_commodity = response.json()

    # Delete the first commodity
    response = client.delete(f"/commodities/{first_commodity.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    # Check that the dataset only has the second commodity
    get_response = client.get(
        "/commodities/",
        headers=normal_user_headers,
        params={"dataset_id": dataset_id},
    )
    assert get_response.status_code == status.HTTP_200_OK

    commodity_list = get_response.json()
    assert len(commodity_list) == 1
    assert commodity_list[0]["name"] == second_commodity["name"]
    assert commodity_list[0]["id"] == second_commodity["id"]
