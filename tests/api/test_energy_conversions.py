from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyConversionCreate, EnergyConversion
from tests.api.test_datasets import get_random_existing_dataset
from tests.api.test_energy_commodities import get_random_existing_energy_commodity
from tests.utils.utils import random_lower_string


def get_random_energy_conversion_create(db: Session) -> EnergyConversionCreate:
    dataset = get_random_existing_dataset(db)
    commodity = get_random_existing_energy_commodity(db)
    return EnergyConversionCreate(
        ref_dataset=dataset.id,
        name=f"Energy Conversion {random_lower_string()}",
        description="Description",
        commodity_unit=commodity.name,
    )


def get_random_existing_energy_conversion(db: Session) -> EnergyConversion:
    create_request = get_random_energy_conversion_create(db)
    return crud.energy_conversion.create(db=db, obj_in=create_request)


def test_create_energy_conversion(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy conversion.
    """
    create_request = get_random_energy_conversion_create(db)
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_commodity = response.json()
    assert created_commodity["component"]["name"] == create_request.name
    assert created_commodity["component"]["description"] == create_request.description
    assert created_commodity["component"]["type"] == EnergyComponentType.CONVERSION.value
    assert created_commodity["commodity_unit"]["name"] == create_request.commodity_unit

# TODO Add more test cases
