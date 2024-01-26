from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyStorageCreate, EnergyStorageUpdate

schemas_with_discharge_efficiency_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_discharge_efficiency_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyStorageUpdate, {}),
    (EnergyStorageCreate, {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.STORAGE, "commodity": "bar"}),
]

schemas_with_discharge_efficiency = schemas_with_discharge_efficiency_required + schemas_with_discharge_efficiency_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_discharge_efficiency_optional)
def test_ok_missing_discharge_efficiency(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a discharge efficiency is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_discharge_efficiency_optional)
def test_ok_none_discharge_efficiency(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a discharge efficiency is optional for a schema
    """
    schema(discharge_efficiency=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_discharge_efficiency)
def test_error_on_negative_discharge_efficiency(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a discharge efficiency is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(discharge_efficiency=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("discharge_efficiency",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_discharge_efficiency)
def test_error_on_positive_discharge_efficiency(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a discharge efficiency is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(discharge_efficiency=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("discharge_efficiency",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be less than or equal to 1"
    assert exc_info.value.errors()[0]["type"] == "less_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_discharge_efficiency)
def test_ok_discharge_efficiencys(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a interest rate with everything between 0 and 1 is valid
    """
    schema(discharge_efficiency=0, **data)
    schema(discharge_efficiency=0.5, **data)
    schema(discharge_efficiency=1, **data)
