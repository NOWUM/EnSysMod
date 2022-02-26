from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentUpdate, EnergyComponentCreate

schemas_with_economic_lifetime_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_economic_lifetime_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyComponentUpdate, {}),
    (EnergyComponentCreate,
     {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.SOURCE})
]

schemas_with_economic_lifetime = schemas_with_economic_lifetime_required + schemas_with_economic_lifetime_optional


@pytest.mark.parametrize("schema,data", schemas_with_economic_lifetime_optional)
def test_ok_missing_economic_lifetime(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a economic lifetime is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_economic_lifetime_optional)
def test_ok_none_economic_lifetime(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a economic lifetime unit is optional for a schema
    """
    schema(economic_lifetime=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_economic_lifetime)
def test_error_on_zero_economic_lifetime(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a economic lifetime is not zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(economic_lifetime=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("economic_lifetime",)
    assert exc_info.value.errors()[0]["msg"] == "Economic lifetime must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_economic_lifetime)
def test_error_on_negative_economic_lifetime(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a economic lifetime is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(economic_lifetime=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("economic_lifetime",)
    assert exc_info.value.errors()[0]["msg"] == "Economic lifetime must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_economic_lifetime)
def test_ok_economic_lifetimes(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a economic lifetime with everything over 0 is valid
    """
    schema(economic_lifetime=1, **data)
