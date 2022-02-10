from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_transmission import EnergyTransmissionCreate
from ensysmod.schemas.energy_transmission_distance import EnergyTransmissionDistanceCreate

schemas_with_distances_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyTransmissionCreate, {"name": "test", "description": "bar", "ref_region_from": 42, "ref_region_to": 1337,
                                "ref_dataset": 42, "type": EnergyComponentType.TRANSMISSION, "commodity": "bar"})
]

schemas_with_distances_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_distances = schemas_with_distances_required + schemas_with_distances_optional


@pytest.mark.parametrize("schema,data", schemas_with_distances_optional)
def test_ok_missing_distances(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distances is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_distances_optional)
def test_error_empty_distances(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distances is optional for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(distances=[], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("distances",)
    assert exc_info.value.errors()[0]["msg"] == "List of distances must not be empty."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_distances)
def test_ok_distances(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a distances with everything over 0 is valid
    """
    schema(distances=[EnergyTransmissionDistanceCreate(distance=5, ref_region_to=4, ref_region_from=3)], **data)
