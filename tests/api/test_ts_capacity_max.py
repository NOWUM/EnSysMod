from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import CapacityMaxCreate
from tests.utils import data_generator as data_gen
from tests.utils.utils import random_float_numbers


def get_random_max_capacity_create(db: Session) -> CapacityMaxCreate:
    source = data_gen.fixed_existing_energy_sink(db)
    region = data_gen.fixed_existing_region(db)
    return CapacityMaxCreate(
        ref_dataset=region.ref_dataset,
        component=source.component.name,
        region=region.name,
        max_capacities=random_float_numbers(8760)
    )


def test_create_max_capacity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a max capacity time series.
    """
    create_request = get_random_max_capacity_create(db)
    response = client.post("/max-capacities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["max_capacities"] == create_request.max_capacities
