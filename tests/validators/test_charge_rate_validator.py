from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyStorageCreate, EnergyStorageUpdate

schemas_with_charge_rate_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_charge_rate_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyStorageUpdate, {}),
    (EnergyStorageCreate, {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.STORAGE, "commodity_name": "bar"}),
]

schemas_with_charge_rate = schemas_with_charge_rate_required + schemas_with_charge_rate_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_charge_rate_optional)
def test_ok_missing_charge_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a charge rate is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_charge_rate_optional)
def test_ok_none_charge_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a charge rate is optional for a schema
    """
    schema(charge_rate=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_charge_rate)
def test_error_on_negative_charge_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a charge rate is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(charge_rate=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("charge_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_charge_rate)
def test_error_on_positive_charge_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a charge rate is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(charge_rate=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("charge_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be less than or equal to 1"
    assert exc_info.value.errors()[0]["type"] == "less_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_charge_rate)
def test_ok_charge_rates(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a charge rate with everything between 0 and 1 is valid
    """
    schema(charge_rate=0, **data)
    schema(charge_rate=0.5, **data)
    schema(charge_rate=1, **data)
