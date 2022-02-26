from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentUpdate, EnergyComponentCreate

schemas_with_capacity_per_plant_unit_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_capacity_per_plant_unit_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyComponentUpdate, {}),
    (EnergyComponentCreate,
     {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.SOURCE})
]

schemas_with_capacity_per_plant_unit = schemas_with_capacity_per_plant_unit_required + schemas_with_capacity_per_plant_unit_optional


@pytest.mark.parametrize("schema,data", schemas_with_capacity_per_plant_unit_required)
def test_error_missing_capacity_per_plant_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a capacity per plant unit is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("capacity_per_plant_unit",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_capacity_per_plant_unit_optional)
def test_ok_missing_capacity_per_plant_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a capacity per plant unit is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_capacity_per_plant_unit_optional)
def test_ok_none_capacity_per_plant_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a capacity per plant unit is optional for a schema
    """
    schema(capacity_per_plant_unit=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_capacity_per_plant_unit)
def test_error_on_zero_capacity_per_plant_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a capacity per plant unit is not zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(capacity_per_plant_unit=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("capacity_per_plant_unit",)
    assert exc_info.value.errors()[0]["msg"] == "Capacity per plant per unit must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_capacity_per_plant_unit)
def test_error_on_negative_capacity_per_plant_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a capacity per plant unit is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(capacity_per_plant_unit=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("capacity_per_plant_unit",)
    assert exc_info.value.errors()[0]["msg"] == "Capacity per plant per unit must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_capacity_per_plant_unit)
def test_ok_capacity_per_plant_units(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a capacity per plant unit with everything over 0.001 is valid
    """
    schema(capacity_per_plant_unit=0.001, **data)
