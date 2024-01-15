from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyCommodityUpdate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import commodity_create_request, new_commodity
from tests.utils.utils import random_string


def test_get_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a commodity.
    """
    commodity = new_commodity(db, user_header)
    response = client.get(f"/commodities/{commodity.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_commodity = response.json()
    assert retrieved_commodity["name"] == commodity.name
    assert retrieved_commodity["id"] == commodity.id


def test_get_commodity_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all commodities of a dataset.
    """
    dataset = new_dataset(db, user_header)
    commodity1 = new_commodity(db, user_header, dataset_id=dataset.id)
    commodity2 = new_commodity(db, user_header, dataset_id=dataset.id)

    response = client.get("/commodities/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    commodity_list = response.json()
    assert len(commodity_list) == 2
    assert commodity_list[0]["name"] == commodity1.name
    assert commodity_list[0]["id"] == commodity1.id
    assert commodity_list[1]["name"] == commodity2.name
    assert commodity_list[1]["id"] == commodity2.id


def test_create_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy commodity.
    """
    create_request = commodity_create_request(db, user_header)
    response = client.post("/commodities/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_commodity = response.json()
    assert created_commodity["name"] == create_request.name
    assert created_commodity["dataset"]["id"] == create_request.ref_dataset
    assert created_commodity["description"] == create_request.description
    assert created_commodity["unit"] == create_request.unit


def test_create_existing_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy commodity.
    """
    create_request = commodity_create_request(db, user_header)
    response = client.post("/commodities/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/commodities/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_commodity_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy commodity.
    """
    create_request = commodity_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/commodities/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_multiple_commodities_same_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating multiple commodities on the same dataset.
    """
    existing_commodity = new_commodity(db, user_header)
    dataset_id = existing_commodity.dataset.id

    # Create a new commodity on the same dataset
    create_request = commodity_create_request(db, user_header)
    create_request.ref_dataset = dataset_id

    response = client.post("/commodities/", headers=user_header, content=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    second_commodity = response.json()

    # Check that the dataset has two commodities
    get_response = client.get("/commodities/", headers=user_header, params={"dataset_id": dataset_id})
    assert get_response.status_code == status.HTTP_200_OK

    commodity_list = get_response.json()
    assert len(commodity_list) == 2
    assert commodity_list[0]["name"] == existing_commodity.name
    assert commodity_list[0]["id"] == existing_commodity.id
    assert commodity_list[1]["name"] == second_commodity["name"]
    assert commodity_list[1]["id"] == second_commodity["id"]


def test_update_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test updating a commodity.
    """
    existing_commodity = new_commodity(db, user_header)

    update_request = EnergyCommodityUpdate(**jsonable_encoder(existing_commodity))
    update_request.name = f"New Commodity Name-{random_string()}"
    update_request.unit = f"New Commodity Unit-{random_string()}"
    update_request.description = f"New Commodity Description-{random_string()}"

    response = client.put(f"/commodities/{existing_commodity.id}", headers=user_header, content=update_request.json())
    assert response.status_code == status.HTTP_200_OK

    updated_commodity = response.json()
    assert updated_commodity["name"] == update_request.name
    assert updated_commodity["unit"] == update_request.unit
    assert updated_commodity["description"] == update_request.description


def test_remove_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting a commodity.
    """
    # Create two commodities in the same dataset
    commodity1 = new_commodity(db, user_header)
    dataset_id = commodity1.dataset.id
    commodity2 = new_commodity(db, user_header, dataset_id=dataset_id)

    # Delete the first commodity
    response = client.delete(f"/commodities/{commodity1.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    # Check that the dataset only has the second commodity
    get_response = client.get("/commodities/", headers=user_header, params={"dataset_id": dataset_id})
    assert get_response.status_code == status.HTTP_200_OK

    commodity_list = get_response.json()
    assert len(commodity_list) == 1
    assert commodity_list[0]["name"] == commodity2.name
    assert commodity_list[0]["id"] == commodity2.id
