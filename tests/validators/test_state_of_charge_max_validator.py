from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyStorageCreate, EnergyStorageUpdate

schemas_with_state_of_charge_max_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_state_of_charge_max_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyStorageUpdate, {}),
    (EnergyStorageCreate, {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.STORAGE, "commodity": "bar"}),
]

schemas_with_state_of_charge_max = schemas_with_state_of_charge_max_required + schemas_with_state_of_charge_max_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_state_of_charge_max_optional)
def test_ok_missing_state_of_charge_max(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a state of charge max is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_state_of_charge_max_optional)
def test_ok_none_state_of_charge_max(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a state of charge max is optional for a schema
    """
    schema(state_of_charge_max=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_state_of_charge_max)
def test_error_on_negative_state_of_charge_max(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a state of charge max is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(state_of_charge_max=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("state_of_charge_max",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_state_of_charge_max)
def test_error_on_positive_state_of_charge_max(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a state of charge max is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(state_of_charge_max=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("state_of_charge_max",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be less than or equal to 1"
    assert exc_info.value.errors()[0]["type"] == "less_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_state_of_charge_max)
def test_ok_state_of_charge_max(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a state of charge max with everything between 0 and 1 is valid
    """
    schema(state_of_charge_max=0, **data)
    schema(state_of_charge_max=0.5, **data)
    schema(state_of_charge_max=1, **data)
