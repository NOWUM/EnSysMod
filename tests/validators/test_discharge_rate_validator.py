from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_storage import EnergyStorageCreate, EnergyStorageUpdate

schemas_with_discharge_rate_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_discharge_rate_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyStorageUpdate, {}),
    (EnergyStorageCreate,
     {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.STORAGE, "commodity": "bar"})
]

schemas_with_discharge_rate = schemas_with_discharge_rate_required + schemas_with_discharge_rate_optional


@pytest.mark.parametrize("schema,data", schemas_with_discharge_rate_optional)
def test_ok_missing_discharge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a discharge rate is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_discharge_rate_optional)
def test_ok_none_discharge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a discharge rate is optional for a schema
    """
    schema(discharge_rate=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_discharge_rate)
def test_error_on_negative_discharge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a discharge rate is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(discharge_rate=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("discharge_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Discharge rate must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_discharge_rate)
def test_error_on_positive_discharge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a discharge rate is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(discharge_rate=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("discharge_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Discharge rate must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_discharge_rate)
def test_ok_discharge_rates(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a discharge rate with everything between 0 and 1 is valid
    """
    schema(discharge_rate=0, **data)
    schema(discharge_rate=0.5, **data)
    schema(discharge_rate=1, **data)
