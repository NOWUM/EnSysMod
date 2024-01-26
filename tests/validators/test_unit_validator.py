from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyCommodityCreate, EnergyCommodityUpdate

schemas_with_unit_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyCommodityCreate, {"name": "test", "description": "foo", "ref_dataset": 42}),
]

schemas_with_unit_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyCommodityUpdate, {}),
]

schemas_with_unit = schemas_with_unit_required + schemas_with_unit_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_unit_required)
def test_error_missing_unit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a unit is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("unit",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_unit_optional)
def test_ok_missing_unit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a unit is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_unit)
def test_error_long_unit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a unit is not longer than 255 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(unit="a" * 256, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("unit",)
    assert exc_info.value.errors()[0]["msg"] == "String should have at most 255 characters"
    assert exc_info.value.errors()[0]["type"] == "string_too_long"


@pytest.mark.parametrize(("schema", "data"), schemas_with_unit)
def test_ok_units(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a unit with everything between 1 and 255 characters is valid
    """
    schema(unit="a", **data)
    schema(unit="a" * 255, **data)
