from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyCommodityCreate, EnergyCommodityUpdate
from tests.utils.data_generator.energy_commodities import (
    commodity_create,
    commodity_create_request,
)
from tests.utils.utils import clear_database, random_lower_string


def test_get_all_commodities(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all commodities.
    """
    clear_database(db)
    commodity1 = commodity_create(db, normal_user_headers)
    commodity2 = commodity_create(db, normal_user_headers)

    response = client.get("/commodities/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    commodity_list = response.json()
    assert len(commodity_list) == 2
    assert commodity_list[0]["name"] == commodity1.name
    assert commodity_list[0]["id"] == commodity1.id
    assert commodity_list[1]["name"] == commodity2.name
    assert commodity_list[1]["id"] == commodity2.id


def test_get_all_commodities_specific_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all commodities belonging to a specific dataset.
    """
    clear_database(db)
    commodity1 = commodity_create(db, normal_user_headers)
    commodity2 = commodity_create(db, normal_user_headers)

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


def test_get_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving a commodity.
    """
    commodity = commodity_create(db, normal_user_headers)
    response = client.get(f"/commodities/{commodity.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    retrieved_commodity = response.json()
    assert retrieved_commodity["name"] == commodity.name
    assert retrieved_commodity["id"] == commodity.id


def test_create_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy commodity.
    """
    create_request = commodity_create_request(db, normal_user_headers)
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_commodity = response.json()
    assert created_commodity["name"] == create_request.name
    assert created_commodity["dataset"]["id"] == create_request.ref_dataset
    assert created_commodity["description"] == create_request.description
    assert created_commodity["unit"] == create_request.unit


def test_create_existing_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an existing energy commodity.
    """
    existing_commodity = commodity_create(db, normal_user_headers)
    create_request = EnergyCommodityCreate(**jsonable_encoder(existing_commodity))
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_commodity_unknown_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy commodity.
    """
    create_request = commodity_create_request(db, normal_user_headers)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/commodities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_multiple_commodities_same_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating multiple commodities on the same dataset.
    """
    existing_commodity = commodity_create(db, normal_user_headers)
    dataset_id = existing_commodity.dataset.id

    # Create a new commodity on the same dataset
    create_request = commodity_create_request(db, normal_user_headers)
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


def test_update_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test updating a commodity.
    """
    existing_commodity = commodity_create(db, normal_user_headers)

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


def test_remove_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test deleting a commodity.
    """
    # Create two commodities in the same dataset
    commodity1 = commodity_create(db, normal_user_headers)
    dataset_id = commodity1.dataset.id
    commodity2 = commodity_create(db, normal_user_headers, dataset_id=dataset_id)

    # Delete the first commodity
    response = client.delete(f"/commodities/{commodity1.id}", headers=normal_user_headers)
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
    assert commodity_list[0]["name"] == commodity2.name
    assert commodity_list[0]["id"] == commodity2.id
