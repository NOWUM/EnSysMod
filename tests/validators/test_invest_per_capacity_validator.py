from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentUpdate, EnergyComponentCreate

schemas_with_invest_per_capacity_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_invest_per_capacity_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyComponentUpdate, {}),
    (EnergyComponentCreate, {"name": "test", "ref_dataset": 42, "type": EnergyComponentType.SOURCE})
]

schemas_with_invest_per_capacity = schemas_with_invest_per_capacity_required + schemas_with_invest_per_capacity_optional


@pytest.mark.parametrize("schema,data", schemas_with_invest_per_capacity_optional)
def test_ok_missing_invest_per_capacity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a invest per capacity is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_invest_per_capacity_optional)
def test_ok_none_invest_per_capacity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a invest per capacity is optional for a schema
    """
    schema(invest_per_capacity=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_invest_per_capacity)
def test_error_on_negative_invest_per_capacity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a invest per capacity is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(invest_per_capacity=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("invest_per_capacity",)
    assert exc_info.value.errors()[0]["msg"] == "Invest per capacity must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_invest_per_capacity)
def test_ok_invest_per_capacities(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a invest per capacity with everything over 0 is valid
    """
    schema(invest_per_capacity=0.001, **data)
    schema(invest_per_capacity=0, **data)
    schema(invest_per_capacity=42.0, **data)
