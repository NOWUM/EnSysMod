from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyConversionCreate, EnergyConversionFactorCreate

schemas_with_physical_unit_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (
        EnergyConversionCreate,
        {"name": "foo", "ref_dataset": 42, "conversion_factors": [EnergyConversionFactorCreate(commodity="bar", conversion_factor=0.42)]},
    ),
]

schemas_with_physical_unit_optional: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_physical_unit = schemas_with_physical_unit_required + schemas_with_physical_unit_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_physical_unit_required)
def test_error_missing_physical_unit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a physical unit is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("physical_unit",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_physical_unit_optional)
def test_ok_missing_physical_unit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a physical unit is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_physical_unit)
def test_error_empty_physical_unit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a physical unit is not empty, if specified
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(physical_unit="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("physical_unit",)
    assert exc_info.value.errors()[0]["msg"] == "String should have at least 1 character"
    assert exc_info.value.errors()[0]["type"] == "string_too_short"


@pytest.mark.parametrize(("schema", "data"), schemas_with_physical_unit)
def test_error_long_physical_unit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a physical unit is not longer than 255 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(physical_unit="a" * 256, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("physical_unit",)
    assert exc_info.value.errors()[0]["msg"] == "String should have at most 255 characters"
    assert exc_info.value.errors()[0]["type"] == "string_too_long"


@pytest.mark.parametrize(("schema", "data"), schemas_with_physical_unit)
def test_ok_physical_units(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a physical unit with everything between 1 and 255 characters is valid
    """
    schema(physical_unit="a", **data)
    schema(physical_unit="a" * 255, **data)
