from typing import Any, Dict, List, Tuple, Type

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import (
    EnergyTransmissionDistanceCreate,
    EnergyTransmissionDistanceUpdate,
)

schemas_with_distance_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyTransmissionDistanceCreate, {"ref_dataset": 1, "component": "test", "region": "Region 1", "region_to": "Region 2"}),
    (EnergyTransmissionDistanceUpdate, {}),
]

schemas_with_distance_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_distance = schemas_with_distance_required + schemas_with_distance_optional


@pytest.mark.parametrize("schema,data", schemas_with_distance_optional)
def test_ok_missing_distance(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distance is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_distance_optional)
def test_ok_none_distance(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distance is optional for a schema
    """
    schema(distance=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_distance_required)
def test_error_missing_distance(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distance is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("distance",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_distance)
def test_error_negative_distance(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distance is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(distance=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("distance",)
    assert exc_info.value.errors()[0]["msg"] == "The distance must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_distance)
def test_ok_distances(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a zero or positive distance is valid
    """
    schema(distance=1000, **data)
    schema(distance=0, **data)
