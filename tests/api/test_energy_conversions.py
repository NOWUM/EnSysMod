from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils import data_generator
from tests.utils.assertions import assert_energy_component
from tests.utils.utils import clear_database


def test_get_all_energy_conversions(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all energy converesions.
    """
    clear_database(db)
    conversion1 = data_generator.random_existing_energy_conversion(db)
    conversion2 = data_generator.random_existing_energy_conversion(db)

    response = client.get("/conversions/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    conversion_list = response.json()
    assert len(conversion_list) == 2
    assert conversion_list[0]["component"]["name"] == conversion1.component.name
    assert conversion_list[0]["component"]["id"] == conversion1.component.id
    assert conversion_list[1]["component"]["name"] == conversion2.component.name
    assert conversion_list[1]["component"]["id"] == conversion2.component.id


def test_create_conversion(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy conversion.
    """
    create_request = data_generator.random_energy_conversion_create(db)
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_conversion = response.json()
    assert_energy_component(created_conversion["component"], create_request, EnergyComponentType.CONVERSION)
    assert created_conversion["commodity_unit"]["name"] == create_request.commodity_unit


def test_create_existing_conversion(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing energy conversion.
    """
    create_request = data_generator.random_energy_conversion_create(db)
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_conversion_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy conversion.
    """
    create_request = data_generator.random_energy_conversion_create(db)
    create_request.ref_dataset = 132456  # ungültige Anfrage
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_conversion_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an energy conversion.
    """
    create_request = data_generator.random_energy_conversion_create(db)
    create_request.commodity_unit = "0"  # ungültige Anfrage
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
