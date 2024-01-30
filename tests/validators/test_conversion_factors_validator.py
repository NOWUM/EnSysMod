from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionFactorCreate

schemas_with_conversion_factors_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (
        EnergyConversionCreate,
        {"name": "test", "description": "bar", "ref_dataset": 42, "type": EnergyComponentType.CONVERSION, "physical_unit": "bar"},
    ),
]

schemas_with_conversion_factors_optional: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_conversion_factors = schemas_with_conversion_factors_required + schemas_with_conversion_factors_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factors_optional)
def test_ok_missing_conversion_factors(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factors is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factors_required)
def test_error_empty_conversion_factors(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factors is optional for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(conversion_factors=[], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("conversion_factors",)
    assert exc_info.value.errors()[0]["msg"] == "Value error, List of conversion factors should not be empty"
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factors)
def test_ok_conversion_factors(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factors with everything over 0 is valid
    """
    schema(conversion_factors=[EnergyConversionFactorCreate(commodity_name="bar", conversion_factor=3)], **data)
