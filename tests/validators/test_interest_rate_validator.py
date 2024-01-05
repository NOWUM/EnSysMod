from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponentUpdate

schemas_with_interest_rate_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_interest_rate_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyComponentUpdate, {}),
    (EnergyComponentCreate, {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.SOURCE}),
]

schemas_with_interest_rate = schemas_with_interest_rate_required + schemas_with_interest_rate_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_interest_rate_optional)
def test_ok_missing_interest_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a interest rate is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_interest_rate_optional)
def test_ok_none_interest_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a capacity per plant unit is optional for a schema
    """
    schema(interest_rate=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_interest_rate)
def test_error_on_negative_interest_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a interest rate is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(interest_rate=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("interest_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Interest rate must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_interest_rate)
def test_error_on_positive_interest_rate(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a interest rate is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(interest_rate=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("interest_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Interest rate must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_interest_rate)
def test_ok_interest_rates(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a interest rate with everything between 0 and 1 is valid
    """
    schema(interest_rate=0, **data)
    schema(interest_rate=0.5, **data)
    schema(interest_rate=1, **data)
