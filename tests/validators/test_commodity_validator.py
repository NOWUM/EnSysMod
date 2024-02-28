from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyConversionFactorCreate, EnergySinkCreate, EnergySourceCreate, EnergyStorageCreate, EnergyTransmissionCreate

schemas_with_commodity_name_name_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyConversionFactorCreate, {"conversion_factor": 4.2}),
    (EnergySinkCreate, {"name": "foo", "ref_dataset": 42}),
    (EnergySourceCreate, {"name": "foo", "ref_dataset": 42}),
    (EnergyStorageCreate, {"name": "foo", "ref_dataset": 42}),
    (EnergyTransmissionCreate, {"name": "foo", "ref_dataset": 42}),
]

schemas_with_commodity_name_name_optional: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_commodity_name_name = schemas_with_commodity_name_name_required + schemas_with_commodity_name_name_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_name_name_required)
def test_error_missing_commodity_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity name is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity_name",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_name_name_optional)
def test_ok_missing_commodity_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity name is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_name_name)
def test_error_empty_commodity_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity name is not empty, if specified
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(commodity_name="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity_name",)
    assert exc_info.value.errors()[0]["msg"] == "String should have at least 1 character"
    assert exc_info.value.errors()[0]["type"] == "string_too_short"


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_name_name)
def test_error_long_commodity_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity name is not longer than 255 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(commodity_name="a" * 256, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity_name",)
    assert exc_info.value.errors()[0]["msg"] == "String should have at most 255 characters"
    assert exc_info.value.errors()[0]["type"] == "string_too_long"


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_name_name)
def test_ok_commodity_names(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity name with everything between 1 and 255 characters is valid
    """
    schema(commodity_name="a", **data)
    schema(commodity_name="a" * 255, **data)
