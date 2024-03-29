from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import TransmissionDistanceCreate, TransmissionDistanceUpdate

schemas_with_distance_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (TransmissionDistanceCreate, {"ref_dataset": 1, "component_name": "test", "region_name": "Region 1", "region_to_name": "Region 2"}),
    (TransmissionDistanceUpdate, {}),
]

schemas_with_distance_optional: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_distance = schemas_with_distance_required + schemas_with_distance_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_distance_optional)
def test_ok_missing_distance(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a distance is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_distance_optional)
def test_ok_none_distance(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a distance is optional for a schema
    """
    schema(distance=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_distance_required)
def test_error_missing_distance(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a distance is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("distance",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_distance)
def test_error_negative_distance(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a distance is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(distance=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("distance",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_distance)
def test_ok_distances(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a zero or positive distance is valid
    """
    schema(distance=1000, **data)
    schema(distance=0, **data)
