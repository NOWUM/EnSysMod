from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils.assertions import assert_energy_component
from tests.utils.data_generator.energy_conversions import (
    conversion_create,
    conversion_create_request,
)
from tests.utils.utils import clear_database


def test_get_all_energy_conversions(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all energy converesions.
    """
    clear_database(db)
    conversion1 = conversion_create(db, normal_user_headers)
    conversion2 = conversion_create(db, normal_user_headers)

    response = client.get("/conversions/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    conversion_list = response.json()
    assert len(conversion_list) == 2
    assert conversion_list[0]["component"]["name"] == conversion1.component.name
    assert conversion_list[0]["component"]["id"] == conversion1.component.id
    assert conversion_list[1]["component"]["name"] == conversion2.component.name
    assert conversion_list[1]["component"]["id"] == conversion2.component.id


def test_create_conversion(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy conversion.
    """
    create_request = conversion_create_request(db, normal_user_headers)
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_conversion = response.json()
    assert_energy_component(created_conversion["component"], create_request, EnergyComponentType.CONVERSION)
    assert created_conversion["commodity_unit"]["name"] == create_request.commodity_unit


def test_create_existing_conversion(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an existing energy conversion.
    """
    create_request = conversion_create_request(db, normal_user_headers)
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_conversion_unknown_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy conversion.
    """
    create_request = conversion_create_request(db, normal_user_headers)
    create_request.ref_dataset = 132456  # ungültige Anfrage
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_conversion_unknown_commodity(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an energy conversion.
    """
    create_request = conversion_create_request(db, normal_user_headers)
    create_request.commodity_unit = "0"  # ungültige Anfrage
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
