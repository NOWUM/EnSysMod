from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas.energy_transmission_distance import EnergyTransmissionDistanceCreate

schemas_with_region_to_or_ref_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyTransmissionDistanceCreate, {"distance": 4, "ref_region_from": 42})
]

schemas_with_region_to_or_ref_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_region_to_or_ref = schemas_with_region_to_or_ref_required + schemas_with_region_to_or_ref_optional


@pytest.mark.parametrize("schema,data", schemas_with_region_to_or_ref_required)
def test_error_missing_region_to_or_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a region_to_or_ref is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Either region_to or ref_region_to must be provided."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_region_to_or_ref_optional)
def test_ok_missing_region_to_or_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a region_to_or_ref is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_region_to_or_ref)
def test_error_on_negative_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a region_to_or_ref is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_region_to=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to the region_to must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_region_to_or_ref)
def test_error_on_zero_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a region_to_or_ref is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_region_to=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to the region_to must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_region_to_or_ref)
def test_error_on_long_region_to(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a region_to_or_ref is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(region_to='a' * 101, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "The region_to must not be longer than 100 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_region_to_or_ref)
def test_ok_region_to_or_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a region_to_or_ref with everything over 0 is valid
    """
    schema(region_to='a', **data)
    schema(region_to='a' * 100, **data)
    schema(ref_region_to=1, **data)
