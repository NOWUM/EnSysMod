from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas.energy_transmission_distance import EnergyTransmissionDistanceCreate, \
    EnergyTransmissionDistanceUpdate

schemas_with_distance_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyTransmissionDistanceCreate, {"ref_region_from": 42, "ref_region_to": 1337})
]

schemas_with_distance_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyTransmissionDistanceUpdate, {})
]

schemas_with_distance = schemas_with_distance_required + schemas_with_distance_optional


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


@pytest.mark.parametrize("schema,data", schemas_with_distance_optional)
def test_ok_missing_distance(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distance is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_distance)
def test_error_on_negative_distance(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distance is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(distance=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("distance",)
    assert exc_info.value.errors()[0]["msg"] == "The distance must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_distance)
def test_ok_distance(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distance with everything over 0 is valid
    """
    schema(distance=0, **data)
    schema(distance=1, **data)
