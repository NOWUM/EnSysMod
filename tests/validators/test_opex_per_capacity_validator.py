from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentUpdate, EnergyComponentCreate

schemas_with_opex_per_capacity_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_opex_per_capacity_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyComponentUpdate, {}),
    (EnergyComponentCreate,
     {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.SOURCE})
]

schemas_with_opex_per_capacity = schemas_with_opex_per_capacity_required + schemas_with_opex_per_capacity_optional


@pytest.mark.parametrize("schema,data", schemas_with_opex_per_capacity_optional)
def test_ok_missing_opex_per_capacity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a opex per capacity is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_opex_per_capacity_optional)
def test_ok_none_opex_per_capacity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a opex per capacity is optional for a schema
    """
    schema(opex_per_capacity=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_opex_per_capacity)
def test_error_on_negative_opex_per_capacity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a opex per capacity is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(opex_per_capacity=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("opex_per_capacity",)
    assert exc_info.value.errors()[0]["msg"] == "Opex per capacity must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_opex_per_capacity)
def test_ok_opex_per_capacitys(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a opex per capacity with everything over 0.001 and 0 is valid
    """
    schema(opex_per_capacity=0.001, **data)
    schema(opex_per_capacity=0, **data)
