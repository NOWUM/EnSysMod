from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyCommodityUpdate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import commodity_create_request, new_commodity
from tests.utils.utils import assert_response, random_string


def test_get_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a commodity.
    """
    commodity = new_commodity(db, user_header)
    response = client.get(f"/commodities/{commodity.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), commodity)


def test_get_commodity_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all commodities of a dataset.
    """
    dataset = new_dataset(db, user_header)
    commodity1 = new_commodity(db, user_header, dataset_id=dataset.id)
    commodity2 = new_commodity(db, user_header, dataset_id=dataset.id)

    response = client.get("/commodities/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert_response(response.json()[0], commodity1)
    assert_response(response.json()[1], commodity2)


def test_create_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy commodity.
    """
    create_request = commodity_create_request(db, user_header)
    response = client.post("/commodities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_existing_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy commodity.
    """
    create_request = commodity_create_request(db, user_header)
    response = client.post("/commodities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/commodities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_commodity_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy commodity.
    """
    create_request = commodity_create_request(db, user_header)
    create_request.ref_dataset = 123456  # ungültige Anfrage
    response = client.post("/commodities/", headers=user_header, content=create_request.model_dump_json())
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

    response = client.post("/commodities/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK

    # Check that the dataset has two commodities
    response = client.get("/commodities/", headers=user_header, params={"dataset_id": dataset_id})
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json()[0], existing_commodity)
    assert_response(response.json()[1], create_request)


def test_update_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test updating a commodity.
    """
    existing_commodity = new_commodity(db, user_header)

    update_request = EnergyCommodityUpdate(
        name=f"New Commodity Name-{random_string()}",
        unit=f"New Commodity Unit-{random_string()}",
        description=f"New Commodity Description-{random_string()}",
    )

    response = client.put(f"/commodities/{existing_commodity.id}", headers=user_header, content=update_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK


def test_remove_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting a commodity.
    """
    # Create two commodities in the same dataset
    dataset = new_dataset(db, user_header)
    commodity1 = new_commodity(db, user_header, dataset_id=dataset.id)
    commodity2 = new_commodity(db, user_header, dataset_id=dataset.id)

    # Delete the first commodity
    response = client.delete(f"/commodities/{commodity1.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    # Check that the dataset only has the second commodity
    response = client.get("/commodities/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert_response(response.json()[0], commodity2)
