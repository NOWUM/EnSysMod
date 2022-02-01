from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import CapacityFixCreate
from tests.utils import data_generator as data_gen
from tests.utils.utils import random_float_numbers


def get_random_fix_capacity_create(db: Session) -> CapacityFixCreate:
    source = data_gen.fixed_existing_energy_sink(db)
    region = data_gen.fixed_existing_region(db)
    return CapacityFixCreate(
        ref_dataset=region.ref_dataset,
        component=source.component.name,
        region=region.name,
        fix_capacities=random_float_numbers(8760)
    )


def test_create_fix_capacity(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a fix capacity time series.
    """
    create_request = get_random_fix_capacity_create(db)
    response = client.post("/fix-capacities/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["name"] == create_request.component
    assert created_ts["region"]["name"] == create_request.region
    assert created_ts["fix_capacities"] == create_request.fix_capacities
