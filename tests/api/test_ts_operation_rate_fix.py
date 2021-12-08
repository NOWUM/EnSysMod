from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import OperationRateFixCreate
from tests.utils.utils import random_float_numbers
from tests.utils import data_generator as data_gen


def get_random_fix_operation_rate_create(db: Session) -> OperationRateFixCreate:
    source = data_gen.fixed_existing_energy_sink(db)
    region = data_gen.fixed_existing_region(db)
    return OperationRateFixCreate(
        ref_component=source.component.id,
        ref_region=region.id,
        fix_operation_rates=random_float_numbers()
    )


def test_create_fix_operation_rate(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a fix operation rate time series.
    """
    create_request = get_random_fix_operation_rate_create(db)
    response = client.post("/fix-operation-rates/", headers=normal_user_headers, data=create_request.json())
    print(response.text)
    assert response.status_code == status.HTTP_200_OK

    created_ts = response.json()
    assert created_ts["component"]["id"] == create_request.ref_component
    assert created_ts["region"]["id"] == create_request.ref_region
    assert created_ts["fix_operation_rates"] == create_request.fix_operation_rates
