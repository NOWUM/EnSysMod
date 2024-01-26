from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import (
    DatasetCreate,
    DatasetUpdate,
    EnergyCommodityCreate,
    EnergyCommodityUpdate,
    EnergyComponentCreate,
    EnergyComponentUpdate,
    RegionCreate,
    RegionUpdate,
)
from ensysmod.schemas.energy_model import EnergyModelCreate, EnergyModelUpdate

schemas_with_name_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (DatasetCreate, {"description": "foo"}),
    (EnergyCommodityCreate, {"description": "foo", "unit": "bar", "ref_dataset": 42}),
    (EnergyComponentCreate, {"type": EnergyComponentType.SOURCE, "ref_dataset": 42}),
    (RegionCreate, {"ref_dataset": 42}),
    (EnergyModelCreate, {"ref_dataset": 42}),
]

schemas_with_name_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (DatasetUpdate, {}),
    (EnergyCommodityUpdate, {}),
    (EnergyComponentUpdate, {}),
    (RegionUpdate, {}),
    (EnergyModelUpdate, {}),
]

schemas_with_name = schemas_with_name_required + schemas_with_name_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_name_required)
def test_error_missing_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a name is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("name",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_name_optional)
def test_ok_missing_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a name is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_name)
def test_error_empty_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a name is not empty, if specified
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(name="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("name",)
    assert exc_info.value.errors()[0]["msg"] == "String should have at least 1 character"
    assert exc_info.value.errors()[0]["type"] == "string_too_short"


@pytest.mark.parametrize(("schema", "data"), schemas_with_name)
def test_error_long_name(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a name is not longer than 255 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(name="a" * 256, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("name",)
    assert exc_info.value.errors()[0]["msg"] == "String should have at most 255 characters"
    assert exc_info.value.errors()[0]["type"] == "string_too_long"


@pytest.mark.parametrize(("schema", "data"), schemas_with_name)
def test_ok_names(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a name with everything between 1 and 255 characters is valid
    """
    schema(name="a", **data)
    schema(name="a" * 255, **data)
