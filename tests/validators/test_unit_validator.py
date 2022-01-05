from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyCommodityCreate, EnergyCommodityUpdate

schemas_with_unit_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyCommodityCreate, {"name": "test", "description": "foo", "ref_dataset": 42})
]

schemas_with_unit_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyCommodityUpdate, {})
]

schemas_with_unit = schemas_with_unit_required + schemas_with_unit_optional


@pytest.mark.parametrize("schema,data", schemas_with_unit_required)
def test_error_missing_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a unit is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("unit",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_unit_optional)
def test_ok_missing_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a unit is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_unit)
def test_error_empty_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a unit is not empty, if specified
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(unit="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("unit",)
    assert exc_info.value.errors()[0]["msg"] == "Unit must not be empty."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_unit)
def test_error_long_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a unit is not longer than 100 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(unit="a" * 101, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("unit",)
    assert exc_info.value.errors()[0]["msg"] == "Unit must not be longer than 100 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_unit)
def test_ok_units(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a unit with everything between 1 and 100 characters is valid
    """
    schema(unit="a", **data)
    schema(unit="a" * 100, **data)
