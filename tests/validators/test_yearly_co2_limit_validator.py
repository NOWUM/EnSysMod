from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_model import EnergyModelCreate, EnergyModelUpdate

schemas_with_yearly_co2_limit_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_yearly_co2_limit_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyModelCreate, {"name": "test", "ref_dataset": 42}),
    (EnergyModelUpdate, {})
]

schemas_with_yearly_co2_limit = schemas_with_yearly_co2_limit_required + schemas_with_yearly_co2_limit_optional


@pytest.mark.parametrize("schema,data", schemas_with_yearly_co2_limit_optional)
def test_ok_missing_yearly_co2_limit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a yearly co2 limit is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_yearly_co2_limit_optional)
def test_ok_none_yearly_co2_limit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a yearly co2 limit is optional for a schema
    """
    schema(yearly_co2_limit=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_yearly_co2_limit)
def test_error_on_negative_yearly_co2_limit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a yearly co2 limit is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(yearly_co2_limit=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("yearly_co2_limit",)
    assert exc_info.value.errors()[0]["msg"] == "The yearly co2-limit must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_yearly_co2_limit)
def test_error_on_zero_yearly_co2_limit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a yearly co2 limit is not 0
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(yearly_co2_limit=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("yearly_co2_limit",)
    assert exc_info.value.errors()[0]["msg"] == "The yearly co2-limit must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_yearly_co2_limit)
def test_ok_yearly_co2_limits(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a yearly co2 limit with everything over 0 is valid
    """
    schema(yearly_co2_limit=1, **data)
    schema(yearly_co2_limit=1.5, **data)
